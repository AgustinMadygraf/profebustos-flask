"""
Path: interface_adapters/gateways/contact_repository.py
"""

from abc import ABC, abstractmethod
from src.entities.contact import Contact

class ContactRepository(ABC):
    "Interfaz para operaciones de acceso a datos de contactos."
    @abstractmethod
    def save(self, contact: Contact) -> Contact:
        "Guarda un contacto y retorna el contacto guardado (puede incluir ID generado, etc)."
        pass # pylint: disable=unnecessary-pass

    @abstractmethod
    def get_all(self) -> list[Contact]:
        "Devuelve una lista de todos los contactos."
        pass # pylint: disable=unnecessary-pass
