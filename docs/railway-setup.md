# Railway y Local Setup

Guia practica para configurar el backend Flask en Railway y para desarrollo local.

## Railway (produccion)

### 1) Start Command

En Railway -> Settings -> Deploy:

```
gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 wsgi:app
```

Si usas `Procfile`, debe contener:

```
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 wsgi:app
```

### 2) Variables de entorno (Railway)

Configura estas variables en Railway -> Variables:

Base de datos (preferido):
- `MYSQL_PRIVATE_URL` o `MYSQL_URL`

Alternativa por variables separadas:
- `MYSQLHOST`
- `MYSQLPORT`
- `MYSQLUSER`
- `MYSQLPASSWORD`
- `MYSQLDATABASE`

Seguridad:
- `ORIGIN_VERIFY_SECRET` (mismo valor que Cloudflare inyecta en `X-Origin-Verify`)

Opcional:
- `FLASK_ENV` debe quedar vacio o `production` (no usar `development` en Railway)

### 3) Cloudflare

Revisa que la Transform Rule:
- Matchee `api.profebustos.com.ar` y path `/v1/contact/email`.
- Inyecte el header `X-Origin-Verify` con el secreto.

### 4) Verificacion rapida

```
curl -i https://<app>.up.railway.app/health
curl -i https://<app>.up.railway.app/health/db
curl -i -X OPTIONS https://api.profebustos.com.ar/v1/contact/email -H "Origin: https://profebustos.com.ar" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: content-type"
curl -i -X POST https://api.profebustos.com.ar/v1/contact/email -H "Origin: https://profebustos.com.ar" -H "Content-Type: application/json" -d "{\"name\":\"Test\",\"email\":\"test@test.com\"}"
```

## Local (desarrollo)

### 1) Variables de entorno

Crear `.env.local` (y opcionalmente `.env.remote`) usando `.env.example` como base:

```
MYSQL_HOST=127.0.0.1
MYSQL_USER=<usuario>
MYSQL_PASSWORD=<password>
MYSQL_DB=<database>
ORIGIN_VERIFY_SECRET=<secreto_local>
FLASK_ENV=development
```

### 2) Ejecutar

```
python run.py
```

### 3) Verificacion rapida

```
curl -i http://localhost:5000/health
curl -i -X OPTIONS http://localhost:5000/v1/contact/email -H "Origin: http://localhost:5173" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: content-type"
curl -i -X POST http://localhost:5000/v1/contact/email -H "Origin: http://localhost:5173" -H "Content-Type: application/json" -d "{\"name\":\"Test\",\"email\":\"test@test.com\"}"
```
