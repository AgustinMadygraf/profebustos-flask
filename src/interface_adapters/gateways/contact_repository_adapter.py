"""
Path: src/interface_adapters/gateways/contact_repository_adapter.py
"""

import pymysql

from src.application.errors import ContactCreateFailed, ContactListFailed, DatabaseUnavailable
from src.entities.contact import Contact
from src.interface_adapters.gateways.contact_repository import ContactRepository

class ContactRepositoryAdapter(ContactRepository):
    "Adaptador para usar mysql_client con el caso de uso."
    def __init__(self, client):
        self.mysql_client = client

    def save(self, contact):
        "Guarda un contacto usando mysql_client y retorna el contacto guardado."
        try:
            self.mysql_client.insert_contacto(
                ticket_id=contact.ticket_id,
                name=contact.name,
                email=contact.email,
                company=contact.company,
                message=contact.message,
                page_location=contact.page_location,
                traffic_source=contact.traffic_source,
                ip=contact.ip,
                user_agent=contact.user_agent
            )
            return contact
        except (ConnectionError, TimeoutError, ValueError) as exc:
            raise ContactCreateFailed() from exc
        except pymysql.Error as exc:
            raise DatabaseUnavailable() from exc
        except RuntimeError as exc:
            if "cryptography" in str(exc).lower():
                raise DatabaseUnavailable() from exc
            raise

    def get_all(self):
        "Devuelve una lista de todos los contactos usando mysql_client."
        try:
            rows = self.mysql_client.get_all_contactos()
            contactos = []
            for row in rows:
                contactos.append(Contact(
                    ticket_id=row.get("ticket_id"),
                    name=row.get("name"),
                    email=row.get("email"),
                    company=row.get("company"),
                    message=row.get("message"),
                    page_location=row.get("page_location"),
                    traffic_source=row.get("traffic_source"),
                    ip=row.get("ip"),
                    user_agent=row.get("user_agent"),
                    created_at=row.get("created_at"),
                ))
            return contactos
        except (ConnectionError, TimeoutError, ValueError) as exc:
            raise ContactListFailed() from exc
        except pymysql.Error as exc:
            raise DatabaseUnavailable() from exc
        except RuntimeError as exc:
            if "cryptography" in str(exc).lower():
                raise DatabaseUnavailable() from exc
            raise
