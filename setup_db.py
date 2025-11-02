"""
Path: setup_db.py
"""

from src.infrastructure.pymysql.create_db_if_not_exists import create_database_if_not_exists

if __name__ == "__main__":
    create_database_if_not_exists()
