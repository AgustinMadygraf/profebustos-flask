
"""
Path: src/infrastructure/pymysql/mysql_client.py
"""

import pymysql
from src.shared.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from src.shared.logger_flask_v0 import get_logger

logger = get_logger()

class MySQLClient:
    "Cliente MySQL para operaciones de base de datos."
    def __init__(self, host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = None
        self.connect()

    def connect(self):
        "Establece una nueva conexión a MySQL."
        try:
            if self.connection:
                self.connection.close()
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db,
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("Conexión a MySQL exitosa")
        except Exception as e:
            logger.error("Error de conexión a MySQL: %s", e)
            raise

    def ensure_connection(self):
        "Verifica si la conexión está abierta y la restablece si es necesario."
        try:
            self.connection.ping(reconnect=True)
        except (pymysql.Error, AttributeError):
            self.connect()

    def insert_contacto(self, ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent):
        "Inserta un registro de contacto en la base de datos."
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO contactos (
                        ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """
                cursor.execute(sql, (
                    ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent
                ))
                self.connection.commit()
                logger.info("Contacto insertado correctamente")
        except Exception as e:
            logger.error("Error al insertar contacto: %s", e)
            raise

    def get_all_contactos(self):
        """
        Devuelve una lista de todos los contactos registrados en la base de datos.
        """
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent, created_at
                    FROM contactos
                    ORDER BY created_at DESC
                """
                cursor.execute(sql)
                contactos = cursor.fetchall()
                logger.info("%d contactos recuperados", len(contactos))
                return contactos
        except Exception as e:
            logger.error("Error al obtener contactos: %s", e)
            raise
