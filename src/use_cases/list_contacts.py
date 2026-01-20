"""
Path: src/use_cases/list_contacts.py
"""

from src.application.dtos.contact_dto import ContactDTO


class ListContactsUseCase:
    "Caso de uso para listar contactos."
    def __init__(self, contact_repository):
        self.contact_repository = contact_repository

    def execute(self):
        "Obtiene todos los contactos del repositorio."
        contactos = self.contact_repository.get_all()
        response = []
        for contact in contactos:
            response.append(ContactDTO(
                ticket_id=contact.ticket_id,
                name=contact.name,
                email=contact.email,
                company=contact.company,
                message=contact.message,
                page_location=contact.page_location,
                traffic_source=contact.traffic_source,
                ip=contact.ip,
                user_agent=contact.user_agent,
                created_at=getattr(contact, "created_at", None),
            ))
        return response
