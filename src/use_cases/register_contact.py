"""
Path: src/use_cases/register_contact.py
"""

from src.application.dtos.contact_dto import ContactDTO
from src.entities.contact import Contact
from src.application.ports.id_generator import IdGenerator

class RegisterContactUseCase:
    "Caso de uso para registrar un contacto."
    def __init__(self, contact_repository, id_generator: IdGenerator):
        self.contact_repository = contact_repository
        self.id_generator = id_generator

    def execute(self, name, email, company, message, page_location, traffic_source, ip, user_agent):
        "Registra un nuevo contacto y lo guarda en el repositorio."
        ticket_id = self.id_generator.new_id()
        contact = Contact(
            ticket_id=ticket_id,
            name=name,
            email=email,
            company=company,
            message=message,
            page_location=page_location,
            traffic_source=traffic_source,
            ip=ip,
            user_agent=user_agent
        )
        saved_contact = self.contact_repository.save(contact)
        return ContactDTO(
            ticket_id=saved_contact.ticket_id,
            name=saved_contact.name,
            email=saved_contact.email,
            company=saved_contact.company,
            message=saved_contact.message,
            page_location=saved_contact.page_location,
            traffic_source=saved_contact.traffic_source,
            ip=saved_contact.ip,
            user_agent=saved_contact.user_agent,
            created_at=getattr(saved_contact, "created_at", None),
        )
