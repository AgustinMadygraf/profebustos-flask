"""
Path: src/infrastructure/pymysql/setup.py
"""

import pymysql
from src.infrastructure.pymysql.db_config import load_db_config
from src.shared.logger_flask_v0 import get_logger

class MySQLSetupChecker:
    "Clase para verificar el entorno MySQL usando conexión persistente."
    def __init__(self):
        self.conn = None
        self.logger = get_logger("profebustos.mysqlsetup")

    def connect(self):
        "Establece la conexión persistente si no existe."
        if self.conn is None:
            try:
                db_config = load_db_config()
                self.conn = pymysql.connect(
                    host=db_config["host"],
                    user=db_config["user"],
                    password=db_config["password"],
                    port=db_config["port"],
                    connect_timeout=5
                )
                self.logger.info("✅ Conexión a MySQL exitosa.")
                return True
            except (pymysql.MySQLError, ConnectionError, OSError) as e:
                self.logger.error("❌ Error de conexión a MySQL: %s", e)
                self.conn = None
                return False
        return True

    def close(self):
        "Cierra la conexión persistente."
        if self.conn:
            self.conn.close()
            self.conn = None
            self.logger.info("Conexión a MySQL cerrada.")

    def check_database_exists(self):
        "Verifica la existencia de la base de datos MySQL."
        db_config = load_db_config()
        self.logger.info("Verificando existencia de base de datos '%s'...", db_config["db"])
        if not self.connect():
            return False
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SHOW DATABASES LIKE %s", (db_config["db"],))
                result = cursor.fetchone()
                if result:
                    self.logger.info("✅ La base de datos existe.")
                    return True
                else:
                    self.logger.warning("❌ La base de datos no existe.")
                    return False
        except pymysql.MySQLError as e:
            self.logger.error("❌ Error verificando base de datos: %s", e)
            return False

    def check_table_exists(self, table_name):
        "Verifica la existencia de una tabla específica en la base de datos MySQL."
        db_config = load_db_config()
        self.logger.info("Verificando existencia de tabla '%s' en '%s'...", table_name, db_config["db"])
        if not self.connect():
            return False
        try:
            # Selecciona la base de datos
            self.conn.select_db(db_config["db"])
            with self.conn.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE %s", (table_name,))
                result = cursor.fetchone()
                if result:
                    self.logger.info("✅ La tabla existe.")
                    return True
                else:
                    self.logger.warning("❌ La tabla no existe.")
                    return False
        except pymysql.MySQLError as e:
            self.logger.error("❌ Error verificando tabla: %s", e)
            return False
