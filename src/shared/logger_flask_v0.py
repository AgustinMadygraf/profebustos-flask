"""
Path: src/shared/logger_flask_v0.py
"""

import logging
import sys

class FlaskStyleFormatter(logging.Formatter):
    "Formateador de logs con estilo Flask."
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[41m', # Red background
        'RESET': '\033[0m'
    }

    def __init__(self, use_color=True):
        fmt = '[%(asctime)s] %(levelname)s: %(message)s'
        datefmt = '%H:%M:%S'
        super().__init__(fmt, datefmt)
        self.use_color = use_color

    def format(self, record):
        msg = super().format(record)
        if self.use_color and record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            reset = self.COLORS['RESET']
            msg = f"{color}{msg}{reset}"
        return msg

def supports_color():
    "Determina si el terminal soporta colores."
    # Windows terminal supports ANSI since Win10, but check for compatibility
    if sys.platform != 'win32':
        return sys.stdout.isatty()
    try:
        import colorama
        colorama.init()
        return True
    except ImportError:
        return False

def get_logger(name="profebustos"):
    "Obtiene un logger configurado para la aplicación con estilo Flask."
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = FlaskStyleFormatter(use_color=supports_color())
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
