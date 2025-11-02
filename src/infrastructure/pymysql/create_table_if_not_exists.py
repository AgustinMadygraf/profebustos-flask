"""
Crea la tabla 'conversiones' si no existe.
"""

import pymysql
from src.shared.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from src.shared.logger_flask_v0 import get_logger

logger = get_logger()

def create_table_if_not_exists():
    "Crea la tabla conversiones si no existe."
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversiones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tipo VARCHAR(50) NOT NULL,
                    timestamp VARCHAR(50) NOT NULL,
                    seccion VARCHAR(50) NOT NULL
                );
            """)
            logger.info("Tabla 'conversiones' verificada/creada correctamente.")
        connection.close()
    except Exception as e:
        logger.error("Error al crear la tabla: %s", e)
        raise