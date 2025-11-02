"""
Path: src/interface_adapters/gateways/mysql_conversion_gateway.py
"""

from src.interface_adapters.gateways.conversion_gateway import ConversionGateway

class MySQLConversionGateway(ConversionGateway):
    "Gateway MySQL para la persistencia de Conversion."
    def __init__(self, mysql_client):
        self.mysql_client = mysql_client

    def save(self, conversion):
        self.mysql_client.insert_conversion(
            conversion.tipo,
            conversion.timestamp,
            conversion.seccion
        )

    def get_all(self):
        "Obtiene todos los registros de conversiones."
        return self.mysql_client.get_all_conversions()
