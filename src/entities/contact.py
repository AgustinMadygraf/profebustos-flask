"""
Path: src/entities/contact.py
"""

class Contact:
    "Representa un contacto registrado a traves del formulario."
    def __init__(self, ticket_id, name, email, company, message, page_location, traffic_source, ip, user_agent, created_at=None):
        self.ticket_id = ticket_id
        self.name = name
        self.email = email
        self.company = company
        self.message = message
        self.page_location = page_location
        self.traffic_source = traffic_source
        self.ip = ip
        self.user_agent = user_agent
        self.created_at = created_at

    def to_dict(self):
        "Convierte la instancia de Contact a un diccionario."
        return {
            "ticket_id": self.ticket_id,
            "name": self.name,
            "email": self.email,
            "company": self.company,
            "message": self.message,
            "page_location": self.page_location,
            "traffic_source": self.traffic_source,
            "ip": self.ip,
            "user_agent": self.user_agent,
            "created_at": self.created_at,
        }
