"""
Path: src/entities/conversion.py
"""

class Conversion:
    "Clase que representa una conversión realizada en el sistema."
    def __init__(self, tipo, timestamp, seccion):
        self.tipo = tipo
        self.timestamp = timestamp
        self.seccion = seccion
