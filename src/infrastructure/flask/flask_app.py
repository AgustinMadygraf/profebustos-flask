"""
Path: src/infrastructure/flask/flask_app.py
"""

import re
import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from src.shared.logger_flask_v0 import get_logger

from src.infrastructure.pymysql.mysql_client import MySQLClient

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

# Nuevo endpoint para registrar datos de contacto
@app.route('/v1/contact/email', methods=['POST'])
def registrar_contacto():
    "Registra un contacto recibido vía POST en formato JSON."
    logger.info("Solicitud a /v1/contact/email")
    if not request.is_json:
        logger.warning("Content-Type inválido")
        return jsonify({'success': False, 'error': 'Formato JSON requerido'}), 400
    data = request.get_json()
    # Validación básica
    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    company = str(data.get('company', '')).strip()
    message = str(data.get('message', '')).strip()
    page_location = str(data.get('page_location', '')).strip()
    traffic_source = str(data.get('traffic_source', '')).strip()

    # Normalizar espacios
    name = re.sub(r'\s+', ' ', name)
    company = re.sub(r'\s+', ' ', company)

    # Validaciones mínimas (ahora 'message' puede estar vacío)
    if not name or not email:
        logger.warning("Campos requeridos faltantes")
        return jsonify({'success': False, 'error': 'Faltan campos requeridos'}), 400
    if len(name) > 120 or len(company) > 160 or len(message) > 1200:
        logger.warning("Longitud de campos excedida")
        return jsonify({'success': False, 'error': 'Longitud de campos excedida'}), 400
    # Validación simple de email
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(email_regex, email):
        logger.warning("Formato de email inválido: %s", email)
        return jsonify({'success': False, 'error': 'El correo electrónico tiene un formato inválido'}), 400

    # Limpiar message de HTML básico
    message = re.sub(r'<[^>]+>', '', message)

    # Generar ticket_id
    ticket_id = str(uuid.uuid4())

    # Guardar en MySQL (debes crear la tabla y método adecuado en mysql_client)
    try:
        mysql_client.insert_contacto(
            ticket_id=ticket_id,
            name=name,
            email=email,
            company=company,
            message=message,
            page_location=page_location,
            traffic_source=traffic_source,
            ip=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        logger.info("Contacto registrado: %s %s %s", ticket_id, name, email)
        return jsonify({'success': True, 'ticket_id': ticket_id}), 201
    except (ConnectionError, TimeoutError, ValueError) as e:
        logger.exception("Error al guardar contacto: %s", str(e))
        return jsonify({'success': False, 'error': 'Error al registrar el contacto'}), 500

# Nuevo endpoint para listar contactos registrados
@app.route('/v1/contact/list', methods=['GET'])
def listar_contactos():
    "Devuelve la lista de todos los contactos registrados."
    logger.info("Solicitud a /v1/contact/list")
    try:
        contactos = mysql_client.get_all_contactos()
        # contactos debe ser una lista de dicts con todos los campos relevantes
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
