"""
Path: src/infrastructure/pymysql/mysql_client.py
"""

import os
from urllib.parse import urlparse

import pymysql
from src.shared.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from src.shared.logger_flask_v0 import get_logger
from src.infrastructure.pymysql.create_table_if_not_exists import TableCreator
from src.infrastructure.pymysql.setup import MySQLSetupChecker

logger = get_logger()


def _load_db_config(host=None, user=None, password=None, db=None, port=None):
    env_url = os.getenv("MYSQL_PRIVATE_URL") or os.getenv("MYSQL_URL")
    if env_url:
        parsed = urlparse(env_url)
        return {
            "host": parsed.hostname,
            "user": parsed.username,
            "password": parsed.password,
            "db": parsed.path.lstrip("/"),
            "port": parsed.port or 3306,
        }

    return {
        "host": host or os.getenv("MYSQLHOST") or os.getenv("MYSQL_HOST") or MYSQL_HOST,
        "user": user or os.getenv("MYSQLUSER") or os.getenv("MYSQL_USER") or MYSQL_USER,
        "password": (
            password
            or os.getenv("MYSQLPASSWORD")
            or os.getenv("MYSQL_PASSWORD")
            or os.getenv("MYSQL_ROOT_PASSWORD")
            or MYSQL_PASSWORD
        ),
        "db": (
            db
            or os.getenv("MYSQLDATABASE")
            or os.getenv("MYSQL_DATABASE")
            or os.getenv("MYSQL_DB")
            or MYSQL_DB
        ),
        "port": int(port or os.getenv("MYSQLPORT") or os.getenv("MYSQL_PORT") or 3306),
    }


class MySQLClient:
    "Cliente MySQL para operaciones de base de datos."
    def __init__(self, host=None, user=None, password=None, db=None, port=None):
        config = _load_db_config(host=host, user=user, password=password, db=db, port=port)
        self.host = config["host"]
        self.user = config["user"]
        self.password = config["password"]
        self.db = config["db"]
        self.port = config["port"]
        self.connection = None
        # Lazy init: connect on first use to avoid boot failure when DB is down.

    def connect(self):
        "Establece una nueva conexión a MySQL."
        try:
            if not self.host or not self.user or not self.db:
                raise ConnectionError("Missing MySQL configuration")
            if self.connection:
                self.connection.close()
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db,
                port=self.port,
                connect_timeout=5,
                cursorclass=pymysql.cursors.DictCursor,
            )
            logger.info("Conexión a MySQL exitosa")
        except Exception as e:
            logger.error("Error de conexión a MySQL: %s", e)
            raise

    def ensure_connection(self):
        "Verifica si la conexión está abierta y la restablece si es necesario."
        try:
            if not self.connection:
                self.connect()
                return
            self.connection.ping(reconnect=True)
        except (pymysql.Error, AttributeError):
            self.connect()

    def _ensure_contactos_table(self):
        if os.getenv("AUTO_CREATE_DB") != "true":
            raise
        table_creator = TableCreator()
        table_creator.create_contactos_table()
        checker = MySQLSetupChecker()
        checker.logger.info("=== Verificación de entorno MySQL ===")
        if checker.connect():
            if checker.check_database_exists():
                checker.check_table_exists("contactos")
        checker.close()
        checker.logger.info("=== Fin de la verificación ===")

    def insert_contacto(self, ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent):
        "Inserta un registro de contacto en la base de datos."
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = (
                    "INSERT INTO contactos ("
                    "ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent, created_at"
                    ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())"
                )
                cursor.execute(sql, (
                    ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent
                ))
                self.connection.commit()
                logger.info("Contacto insertado correctamente")
        except pymysql.err.ProgrammingError as e:
            if e.args and e.args[0] == 1146:
                logger.warning("Tabla 'contactos' inexistente, intentando crearla")
                self._ensure_contactos_table()
                return self.insert_contacto(
                    ticket_id, name, email, company, message,
                    page_location, traffic_source, ip, user_agent
                )
            logger.error("Error al insertar contacto: %s", e)
            raise
        except Exception as e:
            logger.error("Error al insertar contacto: %s", e)
            raise

    def get_all_contactos(self):
        "Devuelve una lista de todos los contactos registrados en la base de datos."
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = (
                    "SELECT ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent, created_at "
                    "FROM contactos "
                    "ORDER BY created_at DESC"
                )
                cursor.execute(sql)
                contactos = cursor.fetchall()
                logger.info("%d contactos recuperados", len(contactos))
                return contactos
        except Exception as e:
            logger.error("Error al obtener contactos: %s", e)
            raise
