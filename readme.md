# profebustos-flask

Aplicación Flask para registrar conversiones de usuarios (por ejemplo, clics en el botón de WhatsApp).

## Instalación

1. Clona el repositorio.
2. Crea y activa un entorno virtual:
   ```sh
   git clone https://github.com/AgustinMadygraf/profebustos-flask
   cd profebustos-flask
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```
3. Instala las dependencias:
   ```sh
  python.exe -m pip install -U pip setuptools wheel
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```sh
   python app.py
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
