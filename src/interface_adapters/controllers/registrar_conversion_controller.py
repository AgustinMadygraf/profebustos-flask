"""
Path: src/interface_adapters/controllers/registrar_conversion_controller.py
"""

from src.entities.conversion import Conversion
from src.use_cases.registrar_conversion import RegistrarConversionUseCase
from src.interface_adapters.gateways.mysql_conversion_gateway import MySQLConversionGateway
from src.interface_adapters.presenters.conversion_presenter import ConversionPresenter
from src.infrastructure.pymsql.mysql_client import MySQLClient

class RegistrarConversionController:
    "Controller for handling registrar conversion requests."
    def handle(self, data):
        "Handle the registrar conversion request."
        conversion = Conversion(**data)
        mysql_client = MySQLClient()
        gateway = MySQLConversionGateway(mysql_client)
        presenter = ConversionPresenter()
        use_case = RegistrarConversionUseCase(gateway, presenter)
        return use_case.execute(conversion)
