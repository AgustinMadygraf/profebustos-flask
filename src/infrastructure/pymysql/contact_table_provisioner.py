"""
Path: src/infrastructure/pymysql/contact_table_provisioner.py
"""

import os

from src.infrastructure.pymysql.create_table_if_not_exists import TableCreator
from src.infrastructure.pymysql.setup import MySQLSetupChecker


class ContactTableProvisioner:
    "Provisioner to create or verify the contactos table."
    def ensure_contactos_table(self):
        if os.getenv("AUTO_CREATE_DB") != "true":
            raise RuntimeError("AUTO_CREATE_DB is not enabled")
        table_creator = TableCreator()
        table_creator.create_contactos_table()
        checker = MySQLSetupChecker()
        checker.logger.info("=== Verificacion de entorno MySQL ===")
        if checker.connect():
            if checker.check_database_exists():
                checker.check_table_exists("contactos")
        checker.close()
        checker.logger.info("=== Fin de la verificacion ===")
