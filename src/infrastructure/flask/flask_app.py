"""
Path: src/infrastructure/flask/flask_app.py
"""

import re
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from src.shared.logger_flask_v0 import get_logger

from src.interface_adapters.controllers.registrar_conversion_controller import RegistrarConversionController
from src.interface_adapters.gateways.mysql_conversion_gateway import MySQLConversionGateway
from src.interface_adapters.presenters.conversion_presenter import ConversionPresenter
from src.infrastructure.pymysql.mysql_client import MySQLClient

logger = get_logger("flask_app")

app = Flask(__name__)
CORS(app, origins="*", supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    " Agrega los encabezados CORS necesarios a la respuesta."
    origin = request.headers.get('Origin')
    allowed_origins = ["http://profebustos.com.ar", "http://localhost:5173"]
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
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

# Instancia única de dependencias
mysql_client = MySQLClient()
gateway = MySQLConversionGateway(mysql_client)
presenter = ConversionPresenter()
controller = RegistrarConversionController(gateway, presenter)

# Nueva ruta para ver todas las conversiones
@app.route('/conversiones', methods=['GET'])
def ver_conversiones():
    "Devuelve todos los registros de la tabla conversiones como JSON."
    logger.info("Solicitud a /conversiones")
    try:
        registros = gateway.get_all()
        return jsonify(registros), 200
    except (ConnectionError, OSError, RuntimeError) as e:
        logger.exception("Error al obtener conversiones: %s", str(e))
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error técnico. Detalle: {str(e)}'
        }), 500

@app.route('/registrar_conversion.php', methods=['POST', 'OPTIONS'])
def registrar_conversion():
    "Endpoint para registrar conversiones."
    logger.info("Solicitud a /registrar_conversion.php")
    if request.method == 'OPTIONS':
        logger.info("Preflight OPTIONS recibido")
        return '', 200

    try:
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
        try:
            result = controller.handle(data)
            logger.info("Resultado de conversión: %s", result)
        except (ConnectionError, OSError, RuntimeError) as e:
            logger.exception("Error en RegistrarConversionController: %s", str(e))
            return jsonify({
                'success': False,
                'error': f'Ocurrió un error técnico en el controlador: {str(e)}'
            }), 500

        return jsonify(result)
    except (ValueError, KeyError, TypeError) as e:
        logger.exception("Error de validación en registrar_conversion: %s", str(e))
        return jsonify({
            'success': False,
            'error': 'Datos incompletos o formato inválido'
        }), 400

@app.route('/tabla')
def tabla_index():
    "Ruta para servir el archivo index.html de la tabla."
    ruta_real = os.path.join(app.static_folder, 'tabla')
    return send_from_directory(ruta_real, 'index.html')


# Etiquetas: GET y POST
@app.route('/etiquetas', methods=['GET'])
def obtener_etiquetas():
    "Devuelve una lista dinámica de etiquetas desde la base de datos."
    try:
        etiquetas = mysql_client.get_all_etiquetas()
        return jsonify(etiquetas), 200
    except (ConnectionError, OSError, RuntimeError) as e:
        logger.error("Error al obtener etiquetas: %s", str(e))
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error técnico al obtener etiquetas: {str(e)}'
        }), 500

@app.route('/etiquetas', methods=['POST'])
def crear_etiqueta():
    "Crea una nueva etiqueta en la base de datos."
    if not request.is_json:
        logger.debug("Formato JSON requerido en POST /etiquetas")
        return jsonify({'success': False, 'error': 'Formato JSON requerido'}), 400
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    descripcion = data.get('descripcion', '').strip()
    logger.debug("Datos recibidos: nombre=%s, descripcion=%s", nombre, descripcion)
    if not nombre:
        logger.debug("Nombre de etiqueta vacío en POST /etiquetas")
        return jsonify({'success': False, 'error': 'El nombre es requerido'}), 400
    try:
        # Guardar en la base de datos
        nueva_id = mysql_client.insert_etiqueta(nombre, descripcion)
        logger.info("Etiqueta creada: id=%s, nombre=%s, descripcion=%s", nueva_id, nombre, descripcion)
        return jsonify({'success': True, 'id': nueva_id, 'nombre': nombre, 'descripcion': descripcion}), 201
    except (ConnectionError, OSError, RuntimeError, ValueError) as e:
        logger.error("Error al crear etiqueta: %s", str(e))
        return jsonify({'success': False, 'error': f'No se pudo crear la etiqueta: {str(e)}'}), 500

@app.route('/conversiones/<int:conversion_id>/etiqueta', methods=['POST'])
def asignar_etiqueta_a_conversion(conversion_id):
    """
    Asigna una etiqueta existente a una conversión solo si no tiene etiqueta.
    Espera JSON: { "etiqueta_id": <int> }
    """
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Formato JSON requerido'}), 400
    data = request.get_json()
    etiqueta_id = data.get('etiqueta_id')
    if not etiqueta_id:
        return jsonify({'success': False, 'error': 'etiqueta_id requerido'}), 400

    try:
        # Verifica conversión
        conversion = mysql_client.get_conversion_by_id(conversion_id)
        if not conversion:
            return jsonify({'success': False, 'error': 'Conversión no encontrada'}), 404
        if conversion.get('etiqueta_id'):
            return jsonify({'success': False, 'error': 'La conversión ya tiene etiqueta'}), 409

        # Verifica etiqueta
        etiqueta = mysql_client.get_etiqueta_by_id(etiqueta_id)
        if not etiqueta:
            return jsonify({'success': False, 'error': 'Etiqueta no encontrada'}), 404

        # Actualiza conversión
        mysql_client.update_conversion_etiqueta(conversion_id, etiqueta_id)
        return jsonify({'success': True}), 200
    except (ConnectionError, OSError, RuntimeError, ValueError) as e:
        logger.error("Error al asignar etiqueta: %s", str(e))
        return jsonify({'success': False, 'error': str(e)}), 500

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
