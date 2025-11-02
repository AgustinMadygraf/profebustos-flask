"""
Path: src/interface_adapters/gateways/conversion_gateway.py
"""

class ConversionGateway:
    "Gateway para la persistencia de Conversion."
    def save(self, conversion):
        "Guarda una conversión."
        raise NotImplementedError("Método save debe ser implementado.")
