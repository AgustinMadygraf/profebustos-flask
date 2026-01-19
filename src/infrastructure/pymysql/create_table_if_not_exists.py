"""
Path: src/infrastructure/pymysql/create_table_if_not_exists.py
"""

import pymysql
from src.infrastructure.pymysql.db_config import load_db_config
from src.shared.logger_flask_v0 import get_logger

class TableCreator:
    "Clase para crear/verificar tablas en la base de datos."
    def __init__(self):
        self.logger = get_logger("profebustos.tablecreator")

    def create_contactos_table(self):
        "Crea la tabla 'contactos' si no existe, según el modelo de contacto actual."
        try:
            config = load_db_config()
            connection = pymysql.connect(
                host=config["host"],
                user=config["user"],
                password=config["password"],
                database=config["db"],
                port=config["port"],
                connect_timeout=5,
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE %s", ("contactos",))
                result = cursor.fetchone()
                if not result:
                    cursor.execute("""
                        CREATE TABLE contactos (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            ticket_id VARCHAR(36) NOT NULL,
                            name VARCHAR(120) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            company VARCHAR(160) NULL,
                            message VARCHAR(1200) NOT NULL,
                            page_location VARCHAR(512) NULL,
                            traffic_source VARCHAR(128) NULL,
                            ip VARCHAR(45) NULL,
                            user_agent VARCHAR(512) NULL,
                            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    self.logger.info("La tabla 'contactos' fue creada correctamente.")
                else:
                    self.logger.info("La tabla 'contactos' ya existía.")
            connection.close()
        except Exception as e:
            self.logger.error("Error al crear la tabla 'contactos': %s", e)
            raise
