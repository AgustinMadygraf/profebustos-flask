"""
Path: src/infrastructure/pymysql/create_table_if_not_exists.py
"""

import pymysql
from src.shared.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from src.shared.logger_flask_v0 import get_logger

class TableCreator:
    "Clase para crear/verificar tablas en la base de datos."
    def __init__(self):
        self.logger = get_logger("profebustos.tablecreator")

    def create_conversiones_table(self):
        "Crea la tabla 'conversiones' si no existe y agrega el campo 'web' si falta."
        try:
            connection = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DB,
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE %s", ("conversiones",))
                result = cursor.fetchone()
                if result:
                    self.logger.info("La tabla 'conversiones' ya existía.")
                    # Verifica si el campo 'web' existe
                    cursor.execute("SHOW COLUMNS FROM conversiones LIKE 'web';")
                    web_column = cursor.fetchone()
                    if not web_column:
                        cursor.execute("ALTER TABLE conversiones ADD COLUMN web VARCHAR(255);")
                        self.logger.info("El campo 'web' fue agregado a la tabla 'conversiones'.")
                    else:
                        self.logger.info("El campo 'web' ya existe en la tabla 'conversiones'.")
                else:
                    cursor.execute("""
                        CREATE TABLE conversiones (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            tipo VARCHAR(50) NOT NULL,
                            timestamp VARCHAR(50) NOT NULL,
                            seccion VARCHAR(50) NOT NULL,
                            web VARCHAR(255)
                        );
                    """)
                    self.logger.info("La tabla 'conversiones' fue creada correctamente.")
                # Agregar columna 'puntaje_lead' si no existe
                cursor.execute("SHOW COLUMNS FROM conversiones LIKE 'puntaje_lead';")
                puntaje_lead_column = cursor.fetchone()
                if not puntaje_lead_column:
                    cursor.execute("""
                        ALTER TABLE conversiones
                        ADD COLUMN puntaje_lead TINYINT UNSIGNED DEFAULT NULL;
                    """)
                    self.logger.info("El campo 'puntaje_lead' fue agregado a la tabla 'conversiones'.")
                else:
                    self.logger.info("El campo 'puntaje_lead' ya existe en la tabla 'conversiones'.")
            connection.close()
        except Exception as e:
            self.logger.error("Error al crear la tabla: %s", e)
            raise

    def create_etiquetas_table(self):
        "Crea la tabla 'etiquetas' si no existe."
        try:
            connection = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DB,
                cursorclass=pymysql.cursors.DictCursor
            )
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE %s", ("etiquetas",))
                result = cursor.fetchone()
                if not result:
                    cursor.execute("""
                        CREATE TABLE etiquetas (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            nombre VARCHAR(50) UNIQUE NOT NULL,
                            descripcion VARCHAR(255) NULL
                        );
                    """)
                    self.logger.info("La tabla 'etiquetas' fue creada correctamente.")
                else:
                    self.logger.info("La tabla 'etiquetas' ya existía.")
                # Agregar columna 'etiqueta_id' a conversiones si no existe
                cursor.execute("SHOW COLUMNS FROM conversiones LIKE 'etiqueta_id';")
                etiqueta_id_column = cursor.fetchone()
                if not etiqueta_id_column:
                    cursor.execute("""
                        ALTER TABLE conversiones
                        ADD COLUMN etiqueta_id INT NULL,
                        ADD FOREIGN KEY (etiqueta_id) REFERENCES etiquetas(id);
                    """)
                    self.logger.info("El campo 'etiqueta_id' fue agregado a la tabla 'conversiones'.")
                else:
                    self.logger.info("El campo 'etiqueta_id' ya existe en la tabla 'conversiones'.")
            connection.close()
        except Exception as e:
            self.logger.error("Error al crear la tabla 'etiquetas': %s", e)
            raise
