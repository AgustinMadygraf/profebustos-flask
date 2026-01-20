"""
Path: src/use_cases/list_contacts.py
"""

class ListContactsUseCase:
    "Caso de uso para listar contactos."
    def __init__(self, contact_repository):
        self.contact_repository = contact_repository

    def execute(self):
        "Obtiene todos los contactos del repositorio."
        return self.contact_repository.get_all()
