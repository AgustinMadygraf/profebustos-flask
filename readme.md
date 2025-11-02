# profebustos-flask

Aplicación Flask para registrar conversiones de usuarios (por ejemplo, clics en el botón de WhatsApp).

## Instalación

Consulta la guía completa en [docs/installing.md](docs/installing.md).

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
4. Configura las variables de entorno en `.env` (ver ejemplo en `docs/installing.md`).
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

Todas las respuestas incluyen encabezados CORS para permitir solicitudes desde cualquier origen.
