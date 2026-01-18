# Guía de instalación

## Instalación local

1. **Clona el repositorio:**
   ```sh
   git clone https://github.com/AgustinMadygraf/profebustos-flask
   cd profebustos-flask
   ```

2. **Crea y activa un entorno virtual:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/macOS
   ```

3. **Instala las dependencias:**
   ```sh
   python.exe -m pip install -U pip setuptools wheel
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno:**
   Crea un archivo `.env.local` en la raíz (usa `.env.example` como base) con el siguiente contenido:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=tu_usuario
   MYSQL_PASSWORD=tu_contraseña
   MYSQL_DATABASE=profebustos
   ORIGIN_VERIFY_SECRET=tu_secreto_local
   FLASK_ENV=development
   ```

5. **Inicializa la base de datos:**
   ```sh
   python setup_db.py
   ```

6. **Ejecuta la aplicación:**
   ```sh
   python run.py
   ```
   La API estará disponible en `http://localhost:5000/registrar_conversion.php`.

---

## Instalación en PythonAnywhere

1. **Sube el proyecto a tu cuenta** (puedes usar GitHub o SFTP).

2. **Crea y activa un entorno virtual** en la consola de PythonAnywhere:
   ```sh
   python3.10 -m venv ~/venv-profebustos
   source ~/venv-profebustos/bin/activate
   pip install -U pip setuptools wheel
   pip install -r ~/profebustos-flask/requirements.txt
   ```

3. **Configura las variables de entorno:**
   - Desde la consola de PythonAnywhere, crea el archivo `.env.remote` en la raíz del proyecto con tus credenciales de MySQL:
     ```sh
     cd ~/profebustos-flask
     echo "MYSQL_HOST=tu_usuario.mysql.pythonanywhere-services.com" >> .env.remote
     echo "MYSQL_USER=tu_usuario" >> .env.remote
     echo "MYSQL_PASSWORD=tu_contraseña" >> .env.remote
     echo "MYSQL_DATABASE=tu_base_de_datos" >> .env.remote
     echo "ORIGIN_VERIFY_SECRET=tu_secreto" >> .env.remote
     echo "FLASK_ENV=production" >> .env.remote
     ```

4. **Crea la base de datos en el panel web de PythonAnywhere:**
   - Ve a la sección "Databases" en el dashboard.
   - Elige "MySQL" y crea una nueva base de datos (por ejemplo, `profebustos`).
   - Anota el nombre de host y usuario que te asigna PythonAnywhere.

5. **Inicializa la base de datos y tabla:**
   - En la consola de PythonAnywhere, navega al proyecto y ejecuta:
     ```sh
     cd ~/profebustos-flask
     source ~/venv-profebustos/bin/activate
     python setup_db.py
     ```

6. **Configura el archivo WSGI:**
   - Edita el archivo `var/www/tu_usuario_pythonanywhere_com_wsgi.py` para que apunte a tu aplicación Flask:
     ```python
     import sys
     PROJECT_ROOT = '/home/tu_usuario/profebustos-flask'
     if PROJECT_ROOT not in sys.path:
         sys.path.insert(0, PROJECT_ROOT)
     from src.infrastructure.flask.flask_app import app as application
     ```

7. **Recarga la aplicación web** desde el panel de PythonAnywhere.

8. **La API estará disponible en:**
   ```
   https://tu_usuario.pythonanywhere.com/registrar_conversion.php
   ```

---

## Notas

- Si cambias la estructura de la base de datos, vuelve a ejecutar `setup_db.py`.
- Para pruebas locales, no es necesario usar ngrok si el frontend y backend están en la misma máquina.
- Consulta la [documentación de la API](../docs/API_documentation.md) para detalles de uso.
