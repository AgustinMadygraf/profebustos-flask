# API de contacto por correo

Este documento describe el contrato esperado del backend que procesará las consultas enviadas desde el formulario de contacto por correo electrónico de `profebustos.com.ar`.

## Resumen del flujo


1. El frontend muestra un formulario con los campos `name`, `email`, `company` (opcional) y `message`.
2. Al enviarse, el frontend realiza una solicitud HTTP POST al backend para registrar la consulta. El flujo mailto ya no se utiliza como respaldo.
3. El backend debe validar los datos, persistirlos y despachar un correo transaccional a `VITE_CONTACT_EMAIL` o a la casilla que el equipo determine.


> **Nota:** El flujo mailto ha sido eliminado. El frontend depende exclusivamente del endpoint HTTP para el registro y notificación de la consulta.

## Endpoint

```
POST https://api.profebustos.com.ar/v1/contact/email
```

### Headers


| Clave         | Valor             |
|---------------|-------------------|
| Content-Type  | application/json  |


> **Nota:** Actualmente no se requiere autenticación por API Key desde el frontend.

### Request Body

```jsonc
{
  "name": "Laura Gómez",           // string, longitud 1-120, requerido
  "email": "laura@example.com",    // string, formato email RFC 5322, requerido
  "company": "Industrias GBA",     // string, longitud 0-160, opcional
  "message": "Necesito diagnostico", // string, longitud 1-1200, requerido
  "page_location": "https://profebustos.com.ar/#contacto", // string, opcional
  "traffic_source": "utm_campaign" // string, opcional, ayuda a analítica
}
```

#### Reglas de validación

- Rechazar registros sin `name`, `email` o `message`.
- Normalizar `name` y `company` con `trim()` y colapsar espacios múltiples.
- `message` debe limpiarse de HTML o scripts (escape server-side) antes de persistir/enviar.
- Sugerido limitar el tamaño total del payload a 4 KB.

### Response

```json
{
  "success": true,
  "ticket_id": "ce1a8f6a-56d1-4c32-9f05-226f9ff74d81"
}
```

#### Códigos de estado

| HTTP | Motivo                                                                 |
|------|------------------------------------------------------------------------|
| 201  | Consulta registrada y correo enviado correctamente.                    |
| 202  | Consulta aceptada para procesamiento asíncrono (cola o worker).        |
| 400  | Datos inválidos (detalle en `error`).                                  |
| 401  | `X-Api-Key` ausente o incorrecto.                                      |
| 429  | Límite de rate alcanzado para la IP o email (reintentar más tarde).    |
| 500  | Error inesperado del servidor.                                         |

#### Ejemplo de error

```json
{
  "success": false,
  "error": "El correo electrónico tiene un formato inválido"
}
```

## Recomendaciones de implementación

- Utilizar un servicio transaccional (SendGrid, Mailjet, AWS SES) o SMTP propio con SPF/DKIM configurado.
- Registrar cada solicitud en una base de datos con los campos validados y metadatos (IP, user-agent, timestamp).
- Implementar rate limiting por IP y por email (ej. 5 solicitudes/hora) para evitar spam.
- Responder siempre en menos de 1 segundo; mover envíos lentos a colas asíncronas.
- Firmar las respuestas con un `ticket_id` (UUID) que pueda compartirse con el usuario si necesita seguimiento.

## Integración con el frontend

El frontend puede invocar el endpoint después de construir el `mailto:`:

```ts
fetch(import.meta.env.VITE_CONTACT_API_URL, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name,
    email,
    company,
    message,
    page_location: window.location.href,
    traffic_source: new URLSearchParams(window.location.search).get('utm_source') ?? 'direct'
  })
}).catch(() => {
  // Se recomienda mostrar un mensaje de error accesible al usuario.
});
```


Registrar los estados (éxito/error) con `recordEmailEngagement` para completar la trazabilidad en GA4 y Clarity.

## Checklist para despliegue en Cloudflare

1. Definir variables de entorno:
  - `VITE_CONTACT_EMAIL` (frontend)
  - `VITE_CONTACT_API_URL` (frontend)
  - `CONTACT_API_KEY`, credenciales SMTP o secretos equivalentes en el backend.
2. Configurar reglas de Firewall para limitar el acceso al endpoint solo desde las IPs de Cloudflare.
3. Habilitar HTTPS forzado y TLS 1.3.
4. Añadir monitores (Health Checks) para el endpoint y alertar cuando devuelva `5xx` repetidos.

