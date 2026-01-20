"""
Path: src/use_cases/register_contact.py
"""

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
        return saved_contact
