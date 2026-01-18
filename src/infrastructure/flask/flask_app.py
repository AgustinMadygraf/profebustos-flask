"""
Path: src/infrastructure/flask/flask_app.py
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from src.shared.logger_flask_v0 import get_logger

from src.infrastructure.pymysql.mysql_client import MySQLClient
from src.interface_adapters.gateways.contact_repository_adapter import ContactRepositoryAdapter
from src.interface_adapters.controllers.contact_controller import ContactController
from src.interface_adapters.presenters.contact_presenter import ContactPresenter
from src.use_cases.register_contact import RegisterContactUseCase

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
    secret = os.getenv("ORIGIN_VERIFY_SECRET", "")
    header_value = request.headers.get("X-Origin-Verify", "")
    if not secret or header_value != secret:
        return jsonify({"success": False, "error": "Forbidden"}), 403
    return None

@app.before_request
def enforce_origin_verify():
    if request.method == "OPTIONS":
        return None
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

# Instancia única de dependencias
mysql_client = MySQLClient()

contact_repository = ContactRepositoryAdapter(mysql_client)
register_contact_use_case = RegisterContactUseCase(contact_repository)
contact_controller = ContactController(register_contact_use_case)

# Preflight explícito para la ruta crítica de contacto
@app.route('/v1/contact/email', methods=['OPTIONS'])
def preflight_contact():
    return '', 204

# Nuevo endpoint para registrar datos de contacto
@app.route('/v1/contact/email', methods=['POST'])
def registrar_contacto():
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
    if request.path.startswith("/v1/contact/"):
        logger.info(
            "Request log path=%s status=%s ip=%s ua=%s origin=%s referer=%s",
            request.path,
            response.status_code,
            request.remote_addr,
            request.headers.get("User-Agent"),
            request.headers.get("Origin"),
            request.headers.get("Referer"),
        )
    return response

# Nuevo endpoint para listar contactos registrados
@app.route('/v1/contact/list', methods=['GET'])
def listar_contactos():
    "Devuelve la lista de todos los contactos registrados."
    logger.info("Solicitud a /v1/contact/list")
    try:
        contactos = contact_repository.get_all()
        return jsonify({'success': True, 'contactos': contactos}), 200
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
