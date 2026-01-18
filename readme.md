# profebustos-flask

Aplicación Flask para registrar conversiones de usuarios (por ejemplo, clics en el botón de WhatsApp).

## Instalación

Consulta la guía completa en [docs/installing.md](docs/installing.md).
Guía de despliegue Railway y setup local en [docs/railway-setup.md](docs/railway-setup.md).

### Ejecución rápida local

1. Clona el repositorio:
   ```sh
   git clone https://github.com/AgustinMadygraf/profebustos-flask
   cd profebustos-flask
   ```
2. Crea y activa un entorno virtual:
   ```sh
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/macOS
   ```
3. Instala las dependencias:
   ```sh
   python.exe -m pip install -U pip setuptools wheel
   pip install -r requirements.txt
   ```
4. Configura las variables de entorno en `.env.local` o `.env.remote` (ver `.env.example` y `docs/installing.md`).
5. Inicializa la base de datos:
   ```sh
   python setup_db.py
   ```
6. Ejecuta la aplicación:
   ```sh
   python run.py
   ```

## Endpoints

### Registrar Conversión

- **URL:** `/registrar_conversion.php`
- **Método:** `POST`
- **Content-Type:** `application/json`
- **Body:**
  ```json
  {
    "tipo": "whatsapp",
    "timestamp": "2025-11-02T15:04:05.123Z",
    "seccion": "fab"
  }
  ```
- **Respuestas:**
  - Éxito:  
    ```json
    { "success": true }
    ```
  - Error de duplicado (HTTP 429):  
    ```json
    { "success": false, "error": "Conversión duplicada detectada" }
    ```
  - Error de datos inválidos (HTTP 400):  
    ```json
    { "success": false, "error": "Datos incompletos o formato inválido" }
    ```
  - Error interno (HTTP 500):  
    ```json
    { "success": false, "error": "Ocurrió un error técnico. Intenta nuevamente más tarde." }
    ```

## CORS

CORS restringido a orígenes permitidos (por ejemplo `https://profebustos.com.ar`).

## Produccion en Railway

- Start Command:
  `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 wsgi:app`
- WSGI entrypoint: `wsgi.py` (exporta `app`).
- Variables de entorno DB (Railway MySQL plugin o externa):
  - `MYSQL_PRIVATE_URL` o `MYSQL_URL` (preferido), o bien:
  - `MYSQLHOST`, `MYSQLPORT`, `MYSQLUSER`, `MYSQLPASSWORD`, `MYSQLDATABASE` / `MYSQL_DATABASE`
  - Alternativa legacy: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`
- Seguridad:
  - `ORIGIN_VERIFY_SECRET` (header `X-Origin-Verify` inyectado por Cloudflare).
  - `FLASK_ENV=development` solo en local.

### Checks rapidos (curl)

- Health:
  `curl -i https://<app>.up.railway.app/health`
- Health DB:
  `curl -i https://<app>.up.railway.app/health/db`
- Preflight:
  `curl -i -X OPTIONS https://api.profebustos.com.ar/v1/contact/email -H "Origin: https://profebustos.com.ar" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: content-type"`
- POST:
  `curl -i -X POST https://api.profebustos.com.ar/v1/contact/email -H "Origin: https://profebustos.com.ar" -H "Content-Type: application/json" -d "{\"name\":\"Test\",\"email\":\"test@test.com\"}"`
