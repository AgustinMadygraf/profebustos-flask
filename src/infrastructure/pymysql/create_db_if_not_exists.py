"""
Crea la base de datos si no existe.
"""

import pymysql

from src.shared.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from src.shared.logger_flask_v0 import get_logger

logger = get_logger()

def create_database_if_not_exists():
    "Crea la base de datos MySQL si no existe."
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DB}`;")
            logger.info("Base de datos '%s' verificada/creada correctamente.", MYSQL_DB)
        connection.close()
    except Exception as e:
        logger.error("Error al crear la base de datos: %s", e)
        raise
