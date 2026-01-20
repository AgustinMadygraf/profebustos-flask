"""
Path: src/infrastructure/flask/flask_app.py
"""

import os
import time
import uuid
from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS

from src.shared.logger_flask_v0 import get_logger

from src.infrastructure.pymysql.mysql_client import MySQLClient
from src.interface_adapters.gateways.contact_repository_adapter import ContactRepositoryAdapter
from src.interface_adapters.controllers.contact_controller import ContactController
from src.interface_adapters.presenters.contact_presenter import ContactPresenter
from src.use_cases.register_contact import RegisterContactUseCase
from src.use_cases.list_contacts import ListContactsUseCase
from src.infrastructure.common.uuid_generator import UUIDGenerator

logger = get_logger("flask_app")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024
# CORS explícito para la ruta crítica de contacto
CORS(
    app,
    resources={
        r"/v1/contact/*": {
            "origins": [
                "http://localhost:5173",
                "https://datamaq.com.ar",
                "https://www.datamaq.com.ar",
                "https://profebustos.com.ar",
                "https://www.profebustos.com.ar",
            ],
            "methods": ["POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "X-Origin-Verify"],
            "max_age": 600,
        }
    },
)

def require_cf_header():
    "Middleware para verificar el header X-Origin-Verify en rutas críticas."
    secret = os.getenv("ORIGIN_VERIFY_SECRET", "")
    header_value = request.headers.get("X-Origin-Verify", "")
    if not secret or header_value != secret:
        return jsonify({"success": False, "error": "Forbidden"}), 403
    return None

@app.before_request
def enforce_origin_verify():
    "Middleware para verificar el header X-Origin-Verify en rutas críticas."
    if request.method == "OPTIONS":
        return None
    g.request_id = (
        request.headers.get("CF-RAY")
        or request.headers.get("X-Request-Id")
        or str(uuid.uuid4())
    )
    g.request_start = time.time()
    if (
        os.getenv("FLASK_ENV") == "development"
        and request.headers.get("Origin") == "http://localhost:5173"
    ):
        return None
    if request.path.startswith("/v1/contact/"):
        return require_cf_header()
    return None

@app.route('/')
def hello_world():
    "Ruta principal de la aplicación."
    logger.info("Ruta principal accedida")
    return 'Hola desde Flask!'

@app.route('/health', methods=['GET'])
def health_check():
    "Health check endpoint."
    logger.info("Health check solicitado")
    return jsonify({'success': True, 'ok': True}), 200

@app.route('/health/db', methods=['GET'])
def health_check_db():
    "DB health check endpoint."
    try:
        mysql_client.ensure_connection()
        return jsonify({'success': True, 'ok': True}), 200
    except (ConnectionError, TimeoutError, ValueError) as exc:
        logger.warning("DB health check failed: %s", exc.__class__.__name__)
        return jsonify({
            'success': False,
            'error': 'DB unavailable',
            'error_code': 'DB_UNAVAILABLE'
        }), 503

# Instancia única de dependencias
mysql_client = MySQLClient()

contact_repository = ContactRepositoryAdapter(mysql_client)
id_generator = UUIDGenerator()
register_contact_use_case = RegisterContactUseCase(contact_repository, id_generator)
contact_controller = ContactController(register_contact_use_case)
list_contacts_use_case = ListContactsUseCase(contact_repository)

# Preflight explícito para la ruta crítica de contacto
@app.route('/v1/contact/email', methods=['OPTIONS'])
def preflight_contact():
    "Manejo de preflight CORS para /v1/contact/email."
    return '', 204

# Nuevo endpoint para registrar datos de contacto
@app.route('/v1/contact/email', methods=['POST'])
def registrar_contacto():
    "Endpoint para registrar datos de contacto."
    logger.info("Solicitud a /v1/contact/email")
    if request.content_type != "application/json":
        return jsonify({
            "success": False,
            "error": "Unsupported Media Type",
            "error_code": "UNSUPPORTED_MEDIA_TYPE"
        }), 415
    if request.content_length is not None and request.content_length > 20 * 1024:
        return jsonify({
            "success": False,
            "error": "Payload Too Large",
            "error_code": "PAYLOAD_TOO_LARGE"
        }), 413
    response, status = contact_controller.registrar_contacto(request)
    if response.get('success') and 'contact' in response:
        contact = response.pop('contact')
        return jsonify(ContactPresenter.to_response(contact)), status
    return jsonify(response), status

@app.after_request
def log_request(response):
    "Middleware para loguear detalles de la solicitud."
    if request.path.startswith("/v1/contact/"):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        request_id = getattr(g, "request_id", None)
        elapsed_ms = None
        if getattr(g, "request_start", None) is not None:
            elapsed_ms = int((time.time() - g.request_start) * 1000)
        ip = request.headers.get("CF-Connecting-IP", request.remote_addr)
        ua = request.headers.get("User-Agent", "")
        origin = request.headers.get("Origin", "")
        logger.info(
            "Request log ts=%s path=%s status=%s ip=%s origin=%s ua=%s referer=%s req_id=%s ms=%s",
            timestamp,
            request.path,
            response.status_code,
            ip,
            origin,
            ua,
            request.headers.get("Referer"),
            request_id,
            elapsed_ms,
        )
    if getattr(g, "request_id", None):
        response.headers["X-Request-Id"] = g.request_id
    return response

# Nuevo endpoint para listar contactos registrados
@app.route('/v1/contact/list', methods=['GET'])
def listar_contactos():
    "Devuelve la lista de todos los contactos registrados."
    logger.info("Solicitud a /v1/contact/list")
    try:
        contactos = list_contacts_use_case.execute()
        response_items = [ContactPresenter.to_response_with_created_at(c) for c in contactos]
        return jsonify({'success': True, 'contactos': response_items}), 200
    except (ConnectionError, TimeoutError, ValueError) as e:
        logger.exception("Error al obtener contactos: %s", str(e))
        return jsonify({'success': False, 'error': 'Error al obtener los contactos'}), 500

# Servir archivos estáticos para visualizar contactos
@app.route('/tabla')
def tabla_index():
    "Ruta para servir el archivo index.html de la tabla de contactos."
    ruta_real = os.path.join(app.static_folder, 'tabla')
    return send_from_directory(ruta_real, 'index.html')

@app.errorhandler(404)
def not_found_error(e):
    "Manejo de errores 404."
    logger.warning("Recurso no encontrado: %s", str(e))
    return jsonify({
        'success': False,
        'error': 'Recurso no encontrado (404)',
        'error_code': 'NOT_FOUND'
    }), 404

@app.errorhandler(Exception)
def handle_exception(e):
    "Manejo global de excepciones no capturadas."
    logger.exception("Error inesperado: %s", str(e))
    is_dev = os.getenv("FLASK_ENV") == "development"
    error_message = (
        f'Ocurrió un error técnico. Detalle: {str(e)}'
        if is_dev
        else 'Ocurrió un error técnico.'
    )
    response = jsonify({
        'success': False,
        'error': error_message,
        'error_code': 'INTERNAL_ERROR'
    })
    response.status_code = 500
    return response
