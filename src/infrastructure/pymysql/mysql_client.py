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

    def insert_conversion(self, tipo, timestamp, seccion, web):
        "Inserta un registro de conversión en la base de datos, incluyendo el campo web."
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    INSERT INTO conversiones (tipo, timestamp, seccion, web)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (tipo, timestamp, seccion, web))
                self.connection.commit()
                logger.info("Conversión insertada correctamente")
        except Exception as e:
            logger.error("Error al insertar conversión: %s", e)
            raise

    def get_all_conversions(self):
        "Obtiene todos los registros de la tabla conversiones, incluyendo el objeto etiqueta si corresponde."
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = '''
                    SELECT c.*, e.id as etiqueta_id, e.nombre as etiqueta_nombre, e.descripcion as etiqueta_descripcion
                    FROM conversiones c
                    LEFT JOIN etiquetas e ON c.etiqueta_id = e.id
                    ORDER BY c.id ASC
                '''
                cursor.execute(sql)
                results = cursor.fetchall()
                logger.info("Registros obtenidos correctamente")
                # Armar lista de conversiones con objeto etiqueta si corresponde
                conversiones = []
                for row in results:
                    conv = dict(row)
                    etiqueta = None
                    if conv.get('etiqueta_id'):
                        etiqueta = {
                            'id': conv['etiqueta_id'],
                            'nombre': conv['etiqueta_nombre'],
                            'descripcion': conv['etiqueta_descripcion']
                        }
                    conv['etiqueta'] = etiqueta
                    # Eliminar campos duplicados del join
                    conv.pop('etiqueta_nombre', None)
                    conv.pop('etiqueta_descripcion', None)
                    conversiones.append(conv)
                return conversiones
        except Exception as e:
            logger.error("Error al obtener conversiones: %s", e)
            raise

    def get_all_etiquetas(self):
        "Obtiene todas las etiquetas de la tabla etiquetas."
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM etiquetas ORDER BY id ASC"
                cursor.execute(sql)
                results = cursor.fetchall()
                logger.info("Etiquetas obtenidas correctamente")
                return results
        except Exception as e:
            logger.error("Error al obtener etiquetas: %s", e)
            raise

    def get_connection(self):
        "Devuelve la conexión actual a MySQL, asegurando que esté activa."
        self.ensure_connection()
        return self.connection

    def insert_etiqueta(self, nombre, descripcion):
        "Inserta una nueva etiqueta y devuelve el id."
        self.ensure_connection()
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO etiquetas (nombre, descripcion) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, descripcion))
            self.connection.commit()
            return cursor.lastrowid

    def get_conversion_by_id(self, conversion_id):
        "Obtiene una conversión por su ID."
        self.ensure_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM conversiones WHERE id=%s", (conversion_id,))
            return cursor.fetchone()

    def get_etiqueta_by_id(self, etiqueta_id):
        "Obtiene una etiqueta por su ID."
        self.ensure_connection()
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM etiquetas WHERE id=%s", (etiqueta_id,))
            return cursor.fetchone()

    def update_conversion_etiqueta(self, conversion_id, etiqueta_id):
        "Actualiza la etiqueta de una conversión."
        logger.info("Intentando actualizar etiqueta: conversion_id=%s, etiqueta_id=%s", conversion_id, etiqueta_id)
        self.ensure_connection()
        logger.info("Conexión activa: %s", self.connection.open if self.connection else 'No existe')
        try:
            with self.connection.cursor() as cursor:
                logger.info("Cursor abierto para UPDATE")
                cursor.execute("UPDATE conversiones SET etiqueta_id=%s WHERE id=%s", (etiqueta_id, conversion_id))
                self.connection.commit()
                logger.info("Etiqueta de conversión actualizada correctamente")
        except Exception as e:
            logger.error("Error en update_conversion_etiqueta: %s", e)
            raise
