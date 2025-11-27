# Informe de unificación Flask

## Certezas
- La aplicación Flask ahora se instancia desde un único `create_app` en `src/infrastructure/flask/flask_app.py`, que agrega tanto el blueprint de plantas (SQLAlchemy) como los endpoints de contacto (MySQL).
- El `create_app` carga la configuración de base de datos relacional con `load_db_config`, construye el `SqlAlchemyPlantRepository` y registra el blueprint vía `build_blueprint` para mantener intactas las rutas `/api`.
- Se aplican políticas de CORS a través de `get_cors_origins` y un `after_request` que replica los encabezados previos, por lo que los orígenes configurados siguen vigentes para todas las rutas, incluidos los endpoints de contacto y de plantas.
- Se preservaron los endpoints de diagnóstico (`/health` y `/api/health`), el manejo global de errores y las rutas estáticas para la tabla de contactos.

## Dudas
- El listado de orígenes permitidos ahora proviene de `get_cors_origins` y se combina con `flask_cors.CORS`; si se esperaba seguir usando únicamente los dominios fijos (`https://profebustos.com.ar` y `http://localhost:5173`), convendría validar que las variables de entorno produzcan el mismo resultado.
- Los endpoints de contacto usan `MySQLClient` sin inicialización explícita de parámetros en esta unificación; si el cliente dependía de configuración cargada en otro módulo del proyecto anterior, es necesario confirmar que las variables necesarias siguen presentes en el entorno.
