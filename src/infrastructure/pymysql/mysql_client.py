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
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=db,
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("Conexión a MySQL exitosa")
        except Exception as e:
            logger.error("Error de conexión a MySQL: %s", e)
            raise

    def insert_conversion(self, tipo, timestamp, seccion):
        "Inserta un registro de conversión en la base de datos."
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO conversiones (tipo, timestamp, seccion)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (tipo, timestamp, seccion))
                self.connection.commit()
                logger.info("Conversión insertada correctamente")
        except Exception as e:
            logger.error("Error al insertar conversión: %s", e)
            raise
