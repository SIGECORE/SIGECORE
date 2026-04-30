## 📖 Historia de Usuario

Como residente del conjunto

Quiero que el sistema me permita consultar si una zona común está disponible en una fecha y hora específica, mostrando solo los horarios libres sin conflictos con otras reservas aprobadas

Para saber si puedo reservar el espacio para mi evento sin tener que preguntar manualmente a la administración

## 🔁 Flujo Esperado 

- Se recibe una petición GET en /api/v1/zonas/disponibilidad con parámetros de consulta (zona_id, fecha, hora_inicio, hora_fin).
- Se valida que el usuario esté autenticado.
- Se valida que los parámetros zona_id, fecha, hora_inicio, hora_fin sean obligatorios.
- Se valida que la fecha no sea anterior a la fecha actual.
- Se valida que hora_inicio sea menor que hora_fin.
- Se valida que la zona exista en la tabla zonas_comunes y que su estado sea "disponible".
- Se verifica en la tabla reservas si existe alguna reserva aprobada que solape con el horario solicitado.
- Se retorna una respuesta JSON con código 200 OK indicando si la zona está disponible o no.

## ✅ Criterios de Aceptación

## 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET /api/v1/zonas/disponibilidad para consulta de disponibilidad.
- [ ] Se valida que el usuario esté autenticado.
- [ ] Se valida que los parámetros zona_id, fecha, hora_inicio, hora_fin sean obligatorios.
- [ ] Se valida que la fecha no sea anterior a la fecha actual.
- [ ] Se valida que hora_inicio sea menor que hora_fin.
- [ ] Se valida que la zona exista y esté disponible (no en mantenimiento).

## 2. 📤 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON cuando está disponible:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "La zona está disponible",
  "data": {
    "zona_id": 1,
    "nombre": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "disponible": true
  }
}

- [ ] Se responde cuando NO está disponible:

{
  "success": true,
  "statusCode": 200,
  "message": "La zona no está disponible en el horario solicitado",
  "data": {
    "zona_id": 1,
    "nombre": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "disponible": false,
    "conflicto_con": {
      "id_reserva": 5,
      "usuario": "Carlos Rodríguez",
      "hora_inicio": "14:00",
      "hora_fin": "17:00"
    }
  }
}

- [ ] Respuesta de error por zona no encontrada:

{
  "success": false,
  "statusCode": 404,
  "message": "Zona no encontrada",
  "error": {
    "error_code": "ZONA_NOT_FOUND",
    "details": "No existe una zona común con el ID 99",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por zona en mantenimiento:

{
  "success": false,
  "statusCode": 400,
  "message": "Zona no disponible",
  "error": {
    "error_code": "ZONA_MANTENIMIENTO",
    "details": "La zona común está actualmente en mantenimiento y no puede ser reservada",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🔧 Notas Técnicas

## Reglas de negocio

- Cualquier usuario autenticado puede consultar disponibilidad.
- No se pueden consultar fechas pasadas.
- La hora de inicio debe ser menor que la hora de fin.
- Una zona en estado "mantenimiento" no está disponible para reservas.
- Se consideran reservas con estado "aprobada" para verificar conflictos.
- Hay conflicto si el nuevo horario solapa con una reserva existente.

## Base de datos (tablas zonas_comunes y reservas)

- Verificar que la zona exista y su estado sea "disponible".
- Consultar la tabla reservas para detectar solapamientos con estado "aprobada".
- Un solapamiento ocurre cuando:
- nueva_hora_inicio < reserva_hora_fin Y nueva_hora_fin > reserva_hora_inicio

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- No se requiere rol específico, cualquier usuario autenticado puede consultar.

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, ZONA_NOT_FOUND, ZONA_MANTENIMIENTO, FECHA_INVALIDA, HORARIO_INVALIDO, PARAMETRO_REQUERIDO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta de disponibilidad de zonas

- Método HTTP: GET
- Ruta: /api/v1/zonas/disponibilidad
- Autenticación requerida: Sí (residente o administrador)

## 📤 Ejemplo de Request

- URL:
- GET /api/v1/zonas/disponibilidad?zona_id=1&fecha=2026-05-15&hora_inicio=14:00&hora_fin=18:00

## 📤 Ejemplo de Respuesta JSON Exitosa (Disponible)

{
  "success": true,
  "statusCode": 200,
  "message": "La zona está disponible",
  "data": {
    "zona_id": 1,
    "nombre": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "disponible": true
  }
}

## 📤 Ejemplo de Respuesta JSON Exitosa (No disponible)

{
  "success": true,
  "statusCode": 200,
  "message": "La zona no está disponible en el horario solicitado",
  "data": {
    "zona_id": 1,
    "nombre": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "disponible": false,
    "conflicto_con": {
      "id_reserva": 5,
      "usuario": "Carlos Rodríguez",
      "hora_inicio": "14:00",
      "hora_fin": "17:00"
    }
  }
}

## 📤 Ejemplo de Respuesta JSON Error (404 Not Found)

{
  "success": false,
  "statusCode": 404,
  "message": "Zona no encontrada",
  "error": {
    "error_code": "ZONA_NOT_FOUND",
    "details": "No existe una zona común con el ID 99",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Zona disponible sin reservas existentes

- Precondición: Zona con ID 1 existe y está "disponible". No hay reservas aprobadas para el horario solicitado.
- Acción: Ejecutar GET /api/v1/zonas/disponibilidad?zona_id=1&fecha=2026-05-15&hora_inicio=14:00&hora_fin=18:00.
- Resultado esperado:
- Código HTTP 200 OK
- data.disponible = true
- message = "La zona está disponible"

### ❌ Caso 2: Zona no disponible por reserva existente

- Precondición: Existe una reserva aprobada para la zona 1 el 2026-05-15 de 14:00 a 17:00.
- Acción: Consultar disponibilidad para el mismo día de 14:00 a 18:00.
- Resultado esperado:
- Código HTTP 200 OK
- data.disponible = false
- data.conflicto_con contiene la reserva conflictiva

### ❌ Caso 3: Zona en mantenimiento

- Precondición: Zona con ID 1 tiene estado "mantenimiento".
- Acción: Consultar disponibilidad para cualquier horario.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: ZONA_MANTENIMIENTO

### ❌ Caso 4: Zona no existe

- Precondición: No existe zona con ID 99.
- Acción: Consultar disponibilidad con zona_id=99.
- Resultado esperado:
- Código HTTP 404 Not Found
- error.error_code: ZONA_NOT_FOUND

### ❌ Caso 5: Fecha anterior a la actual

- Precondición: La fecha actual es 2026-04-28.
- Acción: Consultar disponibilidad con fecha=2026-04-27.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: FECHA_INVALIDA

### ❌ Caso 6: Hora inicio mayor o igual a hora fin

- Precondición: Ninguna.
- Acción: Consultar disponibilidad con hora_inicio=18:00 y hora_fin=14:00.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: HORARIO_INVALIDO

### ❌ Caso 7: Parámetros obligatorios faltantes

- Precondición: Ninguna.
- Acción: Consultar disponibilidad sin el parámetro fecha.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: PARAMETRO_REQUERIDO

### ❌ Caso 8: Usuario no autenticado

- Precondición: El cliente no envía token de autenticación.
- Acción: Consultar disponibilidad sin header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- error.error_code: NO_AUTENTICADO

## ✅ Definición de Hecho

- Historia: [HU-008] Consulta de disponibilidad de zonas

## 📦 Alcance Funcional

- [ ] El endpoint GET /api/v1/zonas/disponibilidad está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de zona existente funciona.
- [ ] La validación de zona en mantenimiento funciona.
- [ ] La validación de fecha no pasada funciona.
- [ ] La validación de horario válido funciona.
- [ ] La detección de conflictos de horario funciona correctamente.
- [ ] Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para la detección de conflictos.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.
- [ ] Se probaron diferentes combinaciones de horarios.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, parámetros de consulta y salida.
- [ ] Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 404 para zona no encontrada.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.