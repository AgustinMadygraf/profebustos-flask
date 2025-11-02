"""
Path: src/interface_adapters/controllers/registrar_conversion_controller.py
"""

from src.entities.conversion import Conversion
from src.use_cases.registrar_conversion import RegistrarConversionUseCase
from src.interface_adapters.gateways.conversion_gateway import ConversionGateway
from src.interface_adapters.presenters.conversion_presenter import ConversionPresenter

class RegistrarConversionController:
    "Controller for handling registrar conversion requests."
    def handle(self, data):
        "Handle the registrar conversion request."
        conversion = Conversion(**data)
        gateway = ConversionGateway()
        presenter = ConversionPresenter()
        use_case = RegistrarConversionUseCase(gateway, presenter)
        return use_case.execute(conversion)
