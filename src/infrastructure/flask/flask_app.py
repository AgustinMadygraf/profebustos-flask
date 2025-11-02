"""
Path: src/infrastructure/flask_app.py
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    "Ruta principal que devuelve un saludo."
    return 'Hola desde Flask!'

@app.route('/saludo')
def saludo():
    "Ruta adicional que devuelve otro saludo."
    return '¡Saludos desde otra ruta!'
