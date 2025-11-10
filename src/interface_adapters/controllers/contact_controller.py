"""
Path: interface_adapters/controllers/contact_controller.py
"""

import re

class ContactController:
    "Controller para manejar la lógica de entrada de contactos."
    def __init__(self, register_contact_use_case):
        self.register_contact_use_case = register_contact_use_case

    def registrar_contacto(self, request):
        "Maneja la solicitud para registrar un nuevo contacto."
        if not request.is_json:
            return {'success': False, 'error': 'Formato JSON requerido'}, 400

        data = request.get_json()
        name = str(data.get('name', '')).strip()
        email = str(data.get('email', '')).strip()
        company = str(data.get('company', '')).strip()
        message = str(data.get('message', '')).strip()
        page_location = str(data.get('page_location', '')).strip()
        traffic_source = str(data.get('traffic_source', '')).strip()

        # Normalizar espacios
        name = re.sub(r'\s+', ' ', name)
        company = re.sub(r'\s+', ' ', company)

        # Validaciones mínimas
        if not name or not email:
            return {'success': False, 'error': 'Faltan campos requeridos'}, 400
        if len(name) > 120 or len(company) > 160 or len(message) > 1200:
            return {'success': False, 'error': 'Longitud de campos excedida'}, 400

        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, email):
            return {
                'success': False, 
                'error': 'El correo electrónico tiene un formato inválido'
            }, 400

        # Limpiar message de HTML básico
        message = re.sub(r'<[^>]+>', '', message)

        try:
            contact = self.register_contact_use_case.execute(
                name=name,
                email=email,
                company=company,
                message=message,
                page_location=page_location,
                traffic_source=traffic_source,
                ip=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )
            return {'success': True, 'ticket_id': contact.ticket_id, 'contact': contact}, 201
        except (ConnectionError, TimeoutError, ValueError):
            return {'success': False, 'error': 'Error al registrar el contacto'}, 500
