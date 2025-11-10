"""
Path: interface_adapters/gateways/contact_repository.py
"""

from abc import ABC, abstractmethod
from src.entities.contact import Contact

class ContactRepository(ABC):
    "Interfaz para el repositorio de contactos."
    @abstractmethod
    def insert_contact(self, contact: Contact):
        "Inserta un contacto en el almacenamiento."
        pass # pylint: disable=unnecessary-pass
