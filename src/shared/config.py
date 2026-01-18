"""
Path: src/shared/config.py
"""

import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.remote", override=False)
load_dotenv(".env.local", override=True)

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")
