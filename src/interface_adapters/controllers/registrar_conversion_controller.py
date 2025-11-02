"""
Path: src/interface_adapters/controllers/registrar_conversion_controller.py
"""

from src.entities.conversion import Conversion
from src.use_cases.registrar_conversion import RegistrarConversionUseCase

class RegistrarConversionController:
    def handle(self, data):
        "Handle the registrar conversion request."
        conversion = Conversion(**data)
        use_case = RegistrarConversionUseCase()
        return use_case.execute(conversion)
