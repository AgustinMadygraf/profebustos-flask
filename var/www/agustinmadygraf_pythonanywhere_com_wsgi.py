"""
Path: var/www/agustinmadygraf_pythonanywhere_com_wsgi.py
"""

import sys

PROJECT_ROOT = '/home/agustinmadygraf/profebustos-flask'
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# importa tu app con ruta absoluta de paquete
from src.infrastructure.flask.flask_app import app as application
