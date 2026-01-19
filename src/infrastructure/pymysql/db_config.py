"""
Path: src/infrastructure/pymysql/db_config.py
"""

import os
from urllib.parse import urlparse

from src.shared.config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB


def load_db_config(host=None, user=None, password=None, db=None, port=None):
    "Carga la configuración de la base de datos MySQL desde variables de entorno o parámetros."
    env_url = os.getenv("MYSQL_PRIVATE_URL") or os.getenv("MYSQL_URL")
    if env_url:
        parsed = urlparse(env_url)
        return {
            "host": parsed.hostname,
            "user": parsed.username,
            "password": parsed.password,
            "db": parsed.path.lstrip("/"),
            "port": parsed.port or 3306,
        }

    return {
        "host": host or os.getenv("MYSQLHOST") or os.getenv("MYSQL_HOST") or MYSQL_HOST,
        "user": user or os.getenv("MYSQLUSER") or os.getenv("MYSQL_USER") or MYSQL_USER,
        "password": (
            password
            or os.getenv("MYSQLPASSWORD")
            or os.getenv("MYSQL_PASSWORD")
            or os.getenv("MYSQL_ROOT_PASSWORD")
            or MYSQL_PASSWORD
        ),
        "db": (
            db
            or os.getenv("MYSQLDATABASE")
            or os.getenv("MYSQL_DATABASE")
            or os.getenv("MYSQL_DB")
            or MYSQL_DB
        ),
        "port": int(port or os.getenv("MYSQLPORT") or os.getenv("MYSQL_PORT") or 3306),
    }
