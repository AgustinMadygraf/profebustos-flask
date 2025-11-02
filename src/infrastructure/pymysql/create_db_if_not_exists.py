"""
Crea la base de datos si no existe.
"""

import pymysql
from src.shared.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from src.shared.logger_flask_v0 import get_logger

class DatabaseCreator:
    "Clase para crear/verificar la base de datos MySQL."
    def __init__(self):
        self.logger = get_logger("profebustos.dbcreator")

    def create_database_if_not_exists(self):
        "Crea la base de datos MySQL si no existe y diferencia si fue creada o ya existía."
        try:
            connection = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES LIKE %s", (MYSQL_DB,))
                result = cursor.fetchone()
                if result:
                    self.logger.info("La base de datos '%s' ya existía.", MYSQL_DB)
                else:
                    cursor.execute(f"CREATE DATABASE `{MYSQL_DB}`;")
                    self.logger.info("La base de datos '%s' fue creada correctamente.", MYSQL_DB)
            connection.close()
        except Exception as e:
            self.logger.error("Error al crear la base de datos: %s", e)
            raise
