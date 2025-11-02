"""
Path: src/shared/logger_flask_v0.py
"""

import logging

def get_logger(name="profebustos"):
    "Obtiene un logger configurado para la aplicación."
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
