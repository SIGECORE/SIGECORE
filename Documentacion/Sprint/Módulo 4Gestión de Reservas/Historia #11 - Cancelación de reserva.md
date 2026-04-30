## 📖 Historia de Usuario

Como residente del conjunto

Quiero que el sistema me permita cancelar una reserva que ya no voy a utilizar, siempre que la cancelación se haga con al menos 24 horas de anticipación

Para liberar el espacio para que otros residentes puedan reservarlo y evitar sanciones por cancelaciones tardías

## 🔁 Flujo Esperado

- Se recibe una petición DELETE en /api/v1/reservas/{id} para cancelar una reserva existente.
- Se valida que el usuario esté autenticado.
- Se valida que la reserva exista en la tabla reservas.
- Se valida que el usuario autenticado sea el propietario de la reserva o un administrador.
- Se valida que la reserva no esté ya cancelada.
- Se valida que la reserva no esté en estado "rechazada" (no se puede cancelar lo ya rechazado).
- Se valida que la fecha de la reserva no sea anterior a la fecha actual.
- Si el usuario es residente (no administrador), se valida que la cancelación se haga con al menos 24 horas de anticipación.
- Se actualiza el estado de la reserva a "cancelada".
- Se retorna una respuesta JSON con código 200 OK confirmando la cancelación.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint DELETE /api/v1/reservas/{id} para cancelar reservas.
- [ ] Se valida que el usuario esté autenticado.
- [ ] Se valida que la reserva exista.
- [ ] Se valida que el usuario sea el propietario o administrador.
- [ ] Se valida que la reserva no esté cancelada.
- [ ] Se valida que la reserva no esté rechazada.
- [ ] Se valida la anticipación mínima de 24 horas (para residentes).

### 2. 📤 Estructura de la información

- [ ] Respuesta de cancelación exitosa:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Reserva cancelada exitosamente",
  "data": {
    "id_reserva": 1,
    "id_zona": 1,
    "nombre_zona": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "estado": "cancelada",
    "fecha_cancelacion": "2026-04-29T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por cancelación tardía:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "No se puede cancelar la reserva",
  "error": {
    "error_code": "CANCELACION_TARDIA",
    "details": "Las reservas solo se pueden cancelar con al menos 24 horas de anticipación",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por reserva ya cancelada:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "RESERVA_YA_CANCELADA",
    "details": "La reserva ya se encuentra cancelada",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
## 🔧 Notas Técnicas

## Reglas de negocio

- Un residente solo puede cancelar sus propias reservas.
- Un administrador puede cancelar cualquier reserva (sin restricción de 24 horas).
- No se pueden cancelar reservas con fecha anterior a la actual.
- No se pueden cancelar reservas que ya fueron rechazadas.
- La anticipación mínima es de 24 horas para residentes.
- Si la reserva ya pasó, no se puede cancelar.

## Base de datos (tabla reservas)

- La tabla debe incluir las siguientes columnas adicionales:

- fecha_cancelacion: TIMESTAMP, NULLABLE
- cancelado_por: INT, NULLABLE (FK usuarios.id_usuario)

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- El id_usuario se obtiene del token.
- Verificar que el usuario sea propietario de la reserva o administrador.

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, RESERVA_NOT_FOUND, RESERVA_YA_CANCELADA, RESERVA_RECHAZADA, CANCELACION_TARDIA, FECHA_PASADA, NO_AUTORIZADO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Cancelación de reserva

- Método HTTP: DELETE
- Ruta: /api/v1/reservas/{id}
- Autenticación requerida: Sí (residente propietario o administrador)

## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Reserva cancelada exitosamente",
  "data": {
    "id_reserva": 1,
    "id_zona": 1,
    "nombre_zona": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "estado": "cancelada",
    "fecha_cancelacion": "2026-04-29T10:30:00Z"
  }
}
```
## 📤 Ejemplo de Respuesta JSON Error (400 Bad Request)
```json
{
  "success": false,
  "statusCode": 400,
  "message": "No se puede cancelar la reserva",
  "error": {
    "error_code": "CANCELACION_TARDIA",
    "details": "Las reservas solo se pueden cancelar con al menos 24 horas de anticipación",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Residente cancela su propia reserva con anticipación

- Precondición: Reserva con ID 1 pertenece al usuario autenticado. La fecha de la reserva es 2026-05-15 y hoy es 2026-04-29 (más de 24 horas).
- Acción: Enviar DELETE /api/v1/reservas/1.
- Resultado esperado:
- Código HTTP 200 OK
- data.estado = "cancelada"
- fecha_cancelacion se guarda con la fecha actual

### ✅ Caso 2: Administrador cancela cualquier reserva

- Precondición: Usuario autenticado es administrador. Reserva con ID 2 existe, fecha es 2026-05-15.
- Acción: Enviar DELETE /api/v1/reservas/2.
- Resultado esperado:
- Código HTTP 200 OK
- La reserva se cancela sin validar las 24 horas

### ❌ Caso 3: Cancelación tardía (menos de 24 horas)

- Precondición: Reserva con ID 1 tiene fecha 2026-04-30 a las 10:00. Hoy es 2026-04-29 a las 09:30 (solo 30 minutos de anticipación).
- Acción: Residente intenta cancelar.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: CANCELACION_TARDIA

### ❌ Caso 4: Reserva no existe

- Precondición: No existe reserva con ID 99.
- Acción: Enviar DELETE /api/v1/reservas/99.
- Resultado esperado:
- Código HTTP 404 Not Found
- error.error_code: RESERVA_NOT_FOUND

### ❌ Caso 5: Reserva ya cancelada

- Precondición: Reserva con ID 1 ya tiene estado "cancelada".
- Acción: Intentar cancelarla nuevamente.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: RESERVA_YA_CANCELADA

### ❌ Caso 6: Reserva rechazada

- Precondición: Reserva con ID 1 tiene estado "rechazada".
- Acción: Intentar cancelarla.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: RESERVA_RECHAZADA

### ❌ Caso 7: Residente intenta cancelar reserva de otro residente

- Precondición: Reserva con ID 1 pertenece al usuario con ID 5. Usuario autenticado es ID 6 (residente).
- Acción: Enviar DELETE /api/v1/reservas/1.
- Resultado esperado:
- Código HTTP 403 Forbidden
- error.error_code: NO_AUTORIZADO

### ❌ Caso 8: Fecha de reserva ya pasó

- Precondición: Reserva con ID 1 tiene fecha anterior a la fecha actual.
- Acción: Intentar cancelarla.
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: FECHA_PASADA

## ✅ Definición de Hecho

- Historia: [HU-011] Cancelación de reserva

## 📦 Alcance Funcional

- [ ] El endpoint DELETE /api/v1/reservas/{id} está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de reserva existente funciona.
- [ ] La validación de propietario (residente) funciona.
- [ ] La validación de cancelación tardía (24 horas) funciona.
- [ ] La validación de reserva no cancelada funciona.
- [ ] La validación de reserva no rechazada funciona.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada validación.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint y salida.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para no autorizado.
- [ ] Se devuelve código HTTP 404 para reserva no encontrada.