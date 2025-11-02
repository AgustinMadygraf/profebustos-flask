"""
Path: src/infrastructure/flask/flask_app.py
"""

import re
from flask import Flask, request, jsonify
from flask_cors import CORS  # Agrega esta importación

app = Flask(__name__)
CORS(app, origins=["http://profebustos.com.ar"])  # Configura CORS para el dominio permitido

@app.route('/')
def hello_world():
    "Ruta principal que devuelve un saludo."
    return 'Hola desde Flask!'

@app.route('/saludo')
def saludo():
    "Ruta adicional que devuelve otro saludo."
    return '¡Saludos desde otra ruta!'

@app.route('/info')
def info():
    "Ruta que devuelve información sobre la aplicación."
    return 'Esta es una aplicación Flask de ejemplo.'

# Manejar preflight OPTIONS
@app.route('/api/registrar_conversion.php', methods=['OPTIONS'])
def handle_options():
    "Manejar solicitudes OPTIONS para CORS."
    return '', 200

@app.route('/registrar_conversion.php', methods=['POST', 'OPTIONS'])
def registrar_conversion():
    "Registrar una conversión basada en los datos JSON recibidos."
    if request.method == 'OPTIONS':
        return '', 200

    # Validar que sea POST
    if request.method != 'POST':
        return jsonify({
            'success': False,
            'error': 'Método no permitido'
        }), 405

    # Validar Content-Type
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Datos incompletos o formato inválido'
        }), 400

    # Obtener datos JSON
    data = request.get_json()

    # Validar campos requeridos
    required_fields = ['tipo', 'timestamp', 'seccion']
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            'success': False,
            'error': 'Datos incompletos o formato inválido'
        }), 400

    timestamp = data['timestamp']
    seccion = data['seccion']

    # Validar formato de timestamp (ISO 8601 básico)
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?$'
    if not re.match(iso_pattern, timestamp):
        return jsonify({
            'success': False,
            'error': 'Datos incompletos o formato inválido'
        }), 400

    # Simulación de duplicado (si timestamp termina en "0")
    if timestamp[-1] == '0':
        return jsonify({
            'success': False,
            'error': 'Conversión duplicada detectada'
        }), 429

    # Simulación de error interno (si seccion es "error")
    if seccion == 'error':
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error técnico. Intenta nuevamente más tarde.'
        }), 500

    # Respuesta exitosa
    return jsonify({
        'success': True
    })
