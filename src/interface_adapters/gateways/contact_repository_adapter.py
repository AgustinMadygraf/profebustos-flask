"""
Path: src/interface_adapters/gateways/contact_repository_adapter.py
"""

from src.interface_adapters.gateways.contact_repository import ContactRepository

class ContactRepositoryAdapter(ContactRepository):
    "Adaptador para usar mysql_client con el caso de uso."
    def __init__(self, client):
        self.mysql_client = client

    def insert_contact(self, contact):
        "Inserta un contacto en la base de datos usando mysql_client."
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
