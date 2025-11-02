"""
Path: src/interface_adapters/presenters/conversion_presenter.py
"""

class ConversionPresenter:
    "Presentador para la conversión de registro."
    def present(self, success=True, error=None):
        "Formatea la respuesta del registro de conversión."
        return {
            "success": success,
            "error": error
        }
