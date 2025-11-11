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
CORS(app, origins=["https://profebustos.com.ar", "http://localhost:5173"], supports_credentials=True)

@app.route('/')
def hello_world():
    "Ruta principal de la aplicación."
    logger.info("Ruta principal accedida")
    return 'Hola desde Flask!'

@app.route('/health', methods=['GET'])
def health_check():
    "Health check endpoint."
    logger.info("Health check solicitado")
    return jsonify({'status': 'ok'}), 200

# Instancia única de dependencias
mysql_client = MySQLClient()

contact_repository = ContactRepositoryAdapter(mysql_client)
register_contact_use_case = RegisterContactUseCase(contact_repository)
contact_controller = ContactController(register_contact_use_case)

# Nuevo endpoint para registrar datos de contacto
@app.route('/v1/contact/email', methods=['POST'])
def registrar_contacto():
    logger.info("Solicitud a /v1/contact/email")
    response, status = contact_controller.registrar_contacto(request)
    if response.get('success') and 'contact' in response:
        contact = response.pop('contact')
        return jsonify(ContactPresenter.to_response(contact)), status
    return jsonify(response), status

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
        'error': 'Recurso no encontrado (404)'
    }), 404

@app.errorhandler(Exception)
def handle_exception(e):
    "Manejo global de excepciones no capturadas."
    logger.exception("Error inesperado: %s", str(e))
    response = jsonify({
        'success': False,
        'error': f'Ocurrió un error técnico. Detalle: {str(e)}'
    })
    response.status_code = 500
    return response
