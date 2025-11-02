"""
Path: src/infrastructure/flask/flask_app.py
"""

import re
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.interface_adapters.controllers.registrar_conversion_controller import RegistrarConversionController
from src.shared.logger_flask_v0 import get_logger

logger = get_logger("flask_app")

app = Flask(__name__)
CORS(app, origins=["http://profebustos.com.ar"], supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    " Agrega los encabezados CORS necesarios a la respuesta."
    response.headers["Access-Control-Allow-Origin"] = "http://profebustos.com.ar"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

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

@app.route('/registrar_conversion.php', methods=['POST', 'OPTIONS'])
def registrar_conversion():
    "Endpoint para registrar conversiones."
    logger.info("Solicitud a /registrar_conversion.php")
    if request.method == 'OPTIONS':
        logger.info("Preflight OPTIONS recibido")
        return '', 200

    if request.method != 'POST':
        logger.warning("Método no permitido: %s", request.method)
        return jsonify({
            'success': False,
            'error': 'Método no permitido'
        }), 405

    if not request.is_json:
        logger.warning("Content-Type inválido")
        return jsonify({
            'success': False,
            'error': 'Datos incompletos o formato inválido'
        }), 400

    data = request.get_json()
    required_fields = ['tipo', 'timestamp', 'seccion']
    if not data or not all(field in data for field in required_fields):
        logger.warning("Campos requeridos faltantes")
        return jsonify({
            'success': False,
            'error': 'Datos incompletos o formato inválido'
        }), 400

    timestamp = data['timestamp']
    seccion = data['seccion']

    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?$'
    if not re.match(iso_pattern, timestamp):
        logger.warning("Formato de timestamp inválido: %s", timestamp)
        return jsonify({
            'success': False,
            'error': 'Datos incompletos o formato inválido'
        }), 400

    if timestamp[-1] == '0':
        logger.info("Conversión duplicada detectada")
        return jsonify({
            'success': False,
            'error': 'Conversión duplicada detectada'
        }), 429

    if seccion == 'error':
        logger.error("Error técnico simulado")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error técnico. Intenta nuevamente más tarde.'
        }), 500

    logger.info("Procesando conversión: %s", data)
    controller = RegistrarConversionController()
    result = controller.handle(data)
    logger.info("Resultado de conversión: %s", result)

    return jsonify(result)
