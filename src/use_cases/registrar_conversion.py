"""
Path: src/use_cases/registrar_conversion.py
"""

class RegistrarConversionUseCase:
    "Caso de uso para registrar una conversión."
    def __init__(self, gateway, presenter):
        self.gateway = gateway
        self.presenter = presenter

    def execute(self, conversion):
        "Registra una conversión dada."
        try:
            self.gateway.save(conversion)
            return self.presenter.present(success=True)
        except (ValueError, TypeError, RuntimeError) as e:
            return self.presenter.present(success=False, error=str(e))
