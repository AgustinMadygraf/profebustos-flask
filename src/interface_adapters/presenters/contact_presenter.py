"""
Path: interface_adapters/presenters/contact_presenter.py
"""

class ContactPresenter:
    "Convierte la entidad Contact a un formato serializable para la respuesta HTTP."
    @staticmethod
    def to_response(contact):
        "Convierte una instancia de Contact a un diccionario."
        return {
            "ticket_id": contact.ticket_id,
            "name": contact.name,
            "email": contact.email,
            "company": contact.company,
            "message": contact.message,
            "page_location": contact.page_location,
            "traffic_source": contact.traffic_source,
            "ip": contact.ip,
            "user_agent": contact.user_agent,
        }

    @staticmethod
    def to_response_with_created_at(contact):
        "Convierte una instancia de Contact incluyendo created_at."
        return {
            "ticket_id": contact.ticket_id,
            "name": contact.name,
            "email": contact.email,
            "company": contact.company,
            "message": contact.message,
            "page_location": contact.page_location,
            "traffic_source": contact.traffic_source,
            "ip": contact.ip,
            "user_agent": contact.user_agent,
            "created_at": contact.created_at,
        }
