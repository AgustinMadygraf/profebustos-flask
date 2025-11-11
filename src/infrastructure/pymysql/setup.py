"""
Path: src/infrastructure/pymysql/setup.py
"""

import pymysql
from src.shared import config
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
                self.conn = pymysql.connect(
                    host=config.MYSQL_HOST,
                    user=config.MYSQL_USER,
                    password=config.MYSQL_PASSWORD,
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
        self.logger.info("Verificando existencia de base de datos '%s'...", config.MYSQL_DB)
        if not self.connect():
            return False
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SHOW DATABASES LIKE %s", (config.MYSQL_DB,))
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
        self.logger.info("Verificando existencia de tabla '%s' en '%s'...", table_name, config.MYSQL_DB)
        if not self.connect():
            return False
        try:
            # Selecciona la base de datos
            self.conn.select_db(config.MYSQL_DB)
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
