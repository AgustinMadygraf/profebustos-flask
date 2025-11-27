"""
Path: src/infrastructure/flask/flask_app.py
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from src.shared.logger_flask_v0 import get_logger
from src.shared.config import get_cors_origins

from src.infrastructure.pymysql.mysql_client import MySQLClient
from src.interface_adapters.gateways.contact_repository_adapter import ContactRepositoryAdapter
from src.interface_adapters.controllers.contact_controller import ContactController
from src.interface_adapters.presenters.contact_presenter import ContactPresenter
from src.use_cases.register_contact import RegisterContactUseCase

from src.infrastructure.sqlalchemy.config import load_db_config
from src.infrastructure.sqlalchemy.session import build_session_factory, create_engine_from_config
from src.infrastructure.sqlalchemy.sqlalchemy_plant_repository import SqlAlchemyPlantRepository
from src.interface_adapters.controllers.flask_routes import build_blueprint

logger = get_logger("flask_app")


def create_app() -> Flask:
    """Bootstrap Flask application combining contact and plant APIs."""

    flask_app = Flask(__name__)
    cors_origins = get_cors_origins()
    CORS(flask_app, origins=cors_origins, supports_credentials=True)

    try:
        config = load_db_config()
    except RuntimeError as exc:
        logger.error(
            "No se pudo cargar la configuración de base de datos (revisa .env y variables DB_*).",
            exc_info=exc,
        )
        raise

    engine = create_engine_from_config(config)
    session_factory = build_session_factory(engine)
    repository = SqlAlchemyPlantRepository(session_factory)
    flask_app.register_blueprint(build_blueprint(repository))

    @flask_app.before_request
    def handle_preflight():
        """
        Responde de forma explícita a solicitudes OPTIONS antes de que Flask
        evalúe las rutas. Esto evita errores 405 en peticiones preflight
        cuando el cliente envía métodos no declarados en las vistas.
        """
        if request.method != "OPTIONS":
            return None

        response = flask_app.make_default_options_response()

        origin = request.headers.get("Origin")
        allow_all = "*" in cors_origins

        if allow_all:
            response.headers["Access-Control-Allow-Origin"] = "*"
        elif origin in cors_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"

        response.headers["Access-Control-Allow-Headers"] = request.headers.get(
            "Access-Control-Request-Headers", "Content-Type, Authorization"
        )
        response.headers["Access-Control-Allow-Methods"] = request.headers.get(
            "Access-Control-Request-Method", "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        )
        response.headers["Access-Control-Allow-Credentials"] = "true"

        return response

    @flask_app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")
        allow_all = "*" in cors_origins

        if allow_all:
            response.headers["Access-Control-Allow-Origin"] = "*"
        elif origin in cors_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"

        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,PATCH,DELETE,OPTIONS"
        response.headers["Access-Control-Allow-Credentials"] = "true"

        if request.method == "OPTIONS":
            response.status_code = 200

        return response

    @flask_app.route('/')
    def hello_world():
        "Ruta principal de la aplicación."
        logger.info("Ruta principal accedida")
        return 'Hola desde Flask!'

    @flask_app.route('/health', methods=['GET'])
    def health_check():
        "Health check endpoint."
        logger.info("Health check solicitado")
        return jsonify({'status': 'ok'}), 200

    mysql_client = MySQLClient()
    contact_repository = ContactRepositoryAdapter(mysql_client)
    register_contact_use_case = RegisterContactUseCase(contact_repository)
    contact_controller = ContactController(register_contact_use_case)

    @flask_app.route('/v1/contact/email', methods=['POST'])
    def registrar_contacto():
        logger.info("Solicitud a /v1/contact/email")
        response, status = contact_controller.registrar_contacto(request)
        if response.get('success') and 'contact' in response:
            contact = response.pop('contact')
            return jsonify(ContactPresenter.to_response(contact)), status
        return jsonify(response), status

    @flask_app.route('/v1/contact/list', methods=['GET'])
    def listar_contactos():
        "Devuelve la lista de todos los contactos registrados."
        logger.info("Solicitud a /v1/contact/list")
        try:
            contactos = contact_repository.get_all()
            return jsonify({'success': True, 'contactos': contactos}), 200
        except (ConnectionError, TimeoutError, ValueError) as e:
            logger.exception("Error al obtener contactos: %s", str(e))
            return jsonify({'success': False, 'error': 'Error al obtener los contactos'}), 500

    @flask_app.route('/tabla')
    def tabla_index():
        "Ruta para servir el archivo index.html de la tabla de contactos."
        ruta_real = os.path.join(flask_app.static_folder, 'tabla')
        return send_from_directory(ruta_real, 'index.html')

    @flask_app.route("/api/health", methods=["GET"])  # simple health check
    def api_health_check() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    @flask_app.errorhandler(404)
    def not_found_error(e):
        "Manejo de errores 404."
        logger.warning("Recurso no encontrado: %s", str(e))
        return jsonify({
            'success': False,
            'error': 'Recurso no encontrado (404)'
        }), 404

    @flask_app.errorhandler(Exception)
    def handle_exception(e):
        "Manejo global de excepciones no capturadas."
        logger.exception("Error inesperado: %s", str(e))
        response = jsonify({
            'success': False,
            'error': f'Ocurrió un error técnico. Detalle: {str(e)}'
        })
        response.status_code = 500
        return response

    return flask_app


app = create_app()
