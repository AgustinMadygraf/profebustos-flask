# API Documentation

## Endpoint: Registrar Conversión

Registra una conversión cuando el usuario hace clic en el botón de WhatsApp.

### URL

```
POST https://<subdominio>.ngrok-free.app/api/registrar_conversion.php
```

### Headers

| Key              | Value              |
|------------------|-------------------|
| Content-Type     | application/json  |

### Request Body

```json
{
  "tipo": "whatsapp",           // Tipo de conversión (string)
  "timestamp": "ISO8601",       // Fecha y hora en formato ISO (string)
  "seccion": "fab"              // Sección de la página (string)
}
```

**Ejemplo:**
```json
{
  "tipo": "whatsapp",
  "timestamp": "2025-11-02T15:04:05.123Z",
  "seccion": "fab"
}
```

### Response

#### Éxito

```json
{
  "success": true
}
```

#### Error de duplicado (demasiados intentos)

- **HTTP Status:** 429

```json
{
  "success": false,
  "error": "Conversión duplicada detectada"
}
```

#### Error de datos inválidos

- **HTTP Status:** 400

```json
{
  "success": false,
  "error": "Datos incompletos o formato inválido"
}
```

#### Error interno del servidor

- **HTTP Status:** 500

```json
{
  "success": false,
  "error": "Ocurrió un error técnico. Intenta nuevamente más tarde."
}
```

### Ejemplo de uso en frontend

```typescript
fetch('https://<subdominio>.ngrok-free.app/api/registrar_conversion.php', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    tipo: 'whatsapp',
    timestamp: new Date().toISOString(),
    seccion: 'fab'
  })
})
  .then(async (response) => {
    const data = await response.json();
    // Manejo de respuesta según status
  })
  .catch((err) => {
    // Manejo de error de red
  });
```

---

**Notas:**
- El endpoint debe validar la existencia de la tabla y devolver un error específico si no existe.
- Los mensajes de error pueden ser usados para mostrar alertas al usuario en el frontend.