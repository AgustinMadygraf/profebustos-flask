"""
Path: src/interface_adapters/gateways/contact_repository_adapter.py
"""

from src.entities.contact import Contact
from src.interface_adapters.gateways.contact_repository import ContactRepository

class ContactRepositoryAdapter(ContactRepository):
    "Adaptador para usar mysql_client con el caso de uso."
    def __init__(self, client):
        self.mysql_client = client

    def save(self, contact):
        "Guarda un contacto usando mysql_client y retorna el contacto guardado."
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

    def get_all(self):
        "Devuelve una lista de todos los contactos usando mysql_client."
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
