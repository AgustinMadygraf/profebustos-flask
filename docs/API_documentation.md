# API Documentation

## Endpoint: Registrar Conversión

Registra una conversión cuando el usuario hace clic en el botón de WhatsApp.

---

### URL

```
POST https://<subdominio>.ngrok-free.app/api/registrar_conversion.php
```

### Headers

| Key          | Value             |
|--------------|------------------|
| Content-Type | application/json |

### Request Body

```json
{
  "tipo": "whatsapp",           // string. Valores posibles: "whatsapp" (puede ampliarse en el futuro)
  "timestamp": "YYYY-MM-DDTHH:mm:ss.sssZ", // string. Formato ISO 8601 en UTC (ejemplo: 2025-11-02T15:04:05.123Z)
  "seccion": "fab"              // string. Valores posibles: "fab" (puede ampliarse en el futuro)
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

---

### Response

Las respuestas siempre tendrán el formato:

```json
{
  "success": true|false,
  "error": "<mensaje de error opcional>"
}
```

#### Éxito

- **HTTP Status:** 200
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

#### Error de tabla no existente

- **HTTP Status:** 500
```json
{
  "success": false,
  "error": "Tabla de conversiones no existe"
}
```

---

### Ejemplo de uso en frontend

```typescript
fetch('https://<subdominio>.ngrok-free.app/api/registrar_conversion.php', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    tipo: 'whatsapp',
    timestamp: new Date().toISOString(), // Siempre en UTC
    seccion: 'fab'
  })
})
  .then(async (response) => {
    const data = await response.json();
    switch (response.status) {
      case 200:
        // Conversión registrada correctamente
        break;
      case 429:
        // Conversión duplicada detectada
        break;
      case 400:
        // Datos incompletos o formato inválido
        break;
      case 500:
        // Error técnico o tabla no existe
        break;
      default:
        // Otro error
        break;
    }
  })
  .catch((err) => {
    // Error de red
  });
```

---

### Notas y recomendaciones

- El endpoint valida la existencia de la tabla y devuelve un error específico si no existe.
- Los mensajes de error pueden ser usados para mostrar alertas al usuario en el frontend.
- Se recomienda versionar el endpoint en el futuro (`/api/v1/registrar_conversion.php`).
- El campo `timestamp` debe estar en formato ISO 8601 **en UTC**. Si necesitas mostrar la hora local en el frontend, convierte el valor recibido desde UTC a tu zona horaria.

#### Ejemplo para mostrar la hora local en el frontend

Si recibes un timestamp en UTC y quieres mostrarlo en la hora local de Buenos Aires (UTC-3), puedes hacerlo así:

```typescript
function mostrarHoraLocal(utcString: string): string {
  const fecha = new Date(utcString);
  return fecha.toLocaleString('es-AR', { timeZone: 'America/Argentina/Buenos_Aires' });
}

// Ejemplo de uso:
const horaLocal = mostrarHoraLocal('2025-11-03T00:12:04.254Z');
// horaLocal será "2/11/2025 21:12:04"
```

- Considerar agregar autenticación y protección contra abuso/rate limiting si el endpoint se expone públicamente.