"""
Path: setup_db.py
"""



from src.infrastructure.pymysql.create_db_if_not_exists import DatabaseCreator
from src.infrastructure.pymysql.create_table_if_not_exists import TableCreator
from src.infrastructure.pymysql.setup import MySQLSetupChecker

if __name__ == "__main__":
    db_creator = DatabaseCreator()
    db_creator.create_database_if_not_exists()
    table_creator = TableCreator()
    table_creator.create_contactos_table()
    checker = MySQLSetupChecker()
    checker.logger.info("=== Verificación de entorno MySQL ===")
    if checker.connect():
        if checker.check_database_exists():
            checker.check_table_exists('contactos')
    checker.close()
    checker.logger.info("=== Fin de la verificación ===")
