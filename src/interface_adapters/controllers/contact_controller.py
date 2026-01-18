"""
Path: interface_adapters/controllers/contact_controller.py
"""

import os
import re

from src.shared.logger_flask_v0 import get_logger

logger = get_logger("contact_controller")

class ContactController:
    "Controller para manejar la lógica de entrada de contactos."
    def __init__(self, register_contact_use_case):
        self.register_contact_use_case = register_contact_use_case

    def registrar_contacto(self, request):
        "Maneja la solicitud para registrar un nuevo contacto."
        if not request.is_json:
            return {
                'success': False,
                'error': 'Formato JSON requerido',
                'error_code': 'JSON_REQUIRED'
            }, 400

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
            return {
                'success': False,
                'error': 'Faltan campos requeridos',
                'error_code': 'MISSING_FIELDS'
            }, 400
        if len(name) > 120 or len(company) > 160 or len(message) > 1200:
            return {
                'success': False,
                'error': 'Longitud de campos excedida',
                'error_code': 'FIELD_LENGTH_EXCEEDED'
            }, 400

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
            return {
                'success': False,
                'error': 'Error al registrar el contacto',
                'error_code': 'CONTACT_CREATE_FAILED'
            }, 500
        except Exception as exc:
            exc_module = exc.__class__.__module__
            if exc_module.startswith("pymysql"):
                logger.warning(
                    "DB no disponible al registrar contacto origin=%s path=%s ip=%s ua=%s err=%s",
                    request.headers.get("Origin"),
                    request.path,
                    request.remote_addr,
                    request.headers.get("User-Agent"),
                    exc.__class__.__name__,
                )
                response = {
                    'success': False,
                    'error': 'Servicio temporalmente no disponible',
                    'error_code': 'DB_UNAVAILABLE'
                }
                if os.getenv("FLASK_ENV") == "development":
                    response["error_detail"] = exc.__class__.__name__
                return response, 503
            raise
