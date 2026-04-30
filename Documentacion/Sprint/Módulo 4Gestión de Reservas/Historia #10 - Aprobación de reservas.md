## 📖 Historia de Usuario

Como administrador del conjunto

Quiero que el sistema me muestre una lista de todas las solicitudes de reserva pendientes con los datos del solicitante, la zona, la fecha y el horario solicitado, y que me permita aprobarlas o rechazarlas con un solo clic

Para evitar conflictos de horarios entre diferentes residentes y garantizar el uso ordenado de las zonas comunes

## 🔁 Flujo Esperado

- Se recibe una petición PATCH en /api/v1/reservas/{id}/estado con el nuevo estado (aprobada o rechazada) en el cuerpo de la solicitud.
- Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).
- Se valida que la reserva exista en la tabla reservas.
- Se valida que la reserva esté en estado "pendiente".
- Se valida que el nuevo estado sea "aprobada" o "rechazada".
- Se actualiza el estado de la reserva en la base de datos.
- Se registra la fecha de aprobación/rechazo y el ID del administrador.
- Se retorna una respuesta JSON con código 200 OK y los datos actualizados de la reserva.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET /api/v1/reservas/pendientes para listar solicitudes pendientes.
- [ ] Se expone un endpoint PATCH /api/v1/reservas/{id}/estado para aprobar o rechazar.
- [ ] Se valida que el usuario autenticado sea administrador.
- [ ] Se valida que la reserva exista y esté en estado "pendiente".
- [ ] Se valida que el nuevo estado sea "aprobada" o "rechazada".

### 2. 📤 Estructura de la información

- [ ] Respuesta para GET /api/v1/reservas/pendientes:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Consulta exitosa",
  "data": {
    "pendientes": [
      {
        "id_reserva": 1,
        "solicitante": {
          "id_usuario": 5,
          "nombre": "Carlos Rodríguez",
          "email": "carlos@example.com",
          "telefono": "3009876543"
        },
        "zona": {
          "id_zona": 1,
          "nombre": "Salón Social"
        },
        "fecha": "2026-05-15",
        "hora_inicio": "14:00",
        "hora_fin": "18:00",
        "observaciones": "Cumpleaños familiar",
        "fecha_solicitud": "2026-04-28T10:30:00Z"
      }
    ]
  }
}
```
- [ ] Respuesta para PATCH /api/v1/reservas/{id}/estado exitoso:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Reserva aprobada exitosamente",
  "data": {
    "id_reserva": 1,
    "estado": "aprobada",
    "fecha_aprobacion": "2026-04-29T09:00:00Z",
    "aprobado_por": "Administrador (ID: 1)"
  }
}
```
- [ ] Respuesta de error por reserva no pendiente:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "RESERVA_NO_PENDIENTE",
    "details": "La reserva ya fue procesada anteriormente. Estado actual: aprobada",
    "timestamp": "2026-04-29T09:00:00Z"
  }
}
```
## 🔧 Notas Técnicas

## Reglas de negocio

- Solo los administradores pueden aprobar o rechazar reservas.
- No se puede modificar una reserva que ya fue aprobada o rechazada.
- Al aprobar una reserva, se debe verificar nuevamente disponibilidad (evitar aprobaciones duplicadas).
- Se debe registrar quién aprobó y la fecha de aprobación.

## Base de datos (tabla reservas)

- La tabla debe incluir las siguientes columnas adicionales:

- fecha_aprobacion: TIMESTAMP, NULLABLE
- aprobado_por: INT, NULLABLE (FK usuarios.id_usuario)

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- Verificar que el usuario tenga rol de administrador (id_rol = 1).

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, RESERVA_NOT_FOUND, RESERVA_NO_PENDIENTE, ESTADO_INVALIDO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoints – Aprobación de reservas

- Endpoint 1: Listar reservas pendientes
- Método HTTP: GET
- Ruta: /api/v1/reservas/pendientes
- Autenticación requerida: Sí (solo administradores)

- Endpoint 2: Aprobar o rechazar reserva
- Método HTTP: PATCH
- Ruta: /api/v1/reservas/{id}/estado
- Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Request (Aprobar)

- URL: PATCH /api/v1/reservas/1/estado

- Request Body:
```json
{
  "estado": "aprobada"
}
```
## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Reserva aprobada exitosamente",
  "data": {
    "id_reserva": 1,
    "estado": "aprobada",
    "fecha_aprobacion": "2026-04-29T09:00:00Z",
    "aprobado_por": "Administrador (ID: 1)"
  }
}
```
## 📤 Ejemplo de Respuesta JSON Error (403 Forbidden)
```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "ACCESO_DENEGADO",
    "details": "Se requiere rol de administrador para aprobar reservas",
    "timestamp": "2026-04-29T09:00:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Listar reservas pendientes

- Precondición: Usuario autenticado es administrador. Existen reservas con estado "pendiente".
- Acción: Ejecutar GET /api/v1/reservas/pendientes.
- Resultado esperado:
- Código HTTP 200 OK
- La lista contiene solo reservas con estado "pendiente"

### ✅ Caso 2: Aprobar reserva exitosamente

- Precondición: Usuario autenticado es administrador. Reserva con ID 1 está "pendiente". No hay conflictos de horario.
- Acción: Ejecutar PATCH /api/v1/reservas/1/estado con estado = "aprobada".
- Resultado esperado:
- Código HTTP 200 OK
- data.estado = "aprobada"
- fecha_aprobacion se guarda con la fecha actual
- aprobado_por guarda el ID del administrador

### ✅ Caso 3: Rechazar reserva exitosamente

- Precondición: Reserva con ID 2 está "pendiente".
- Acción: Ejecutar PATCH /api/v1/reservas/2/estado con estado = "rechazada".
- Resultado esperado:
- Código HTTP 200 OK
- data.estado = "rechazada"

### ❌ Caso 4: Reserva no existe

- Precondición: No existe reserva con ID 99.
- Acción: Ejecutar PATCH /api/v1/reservas/99/estado.
- Resultado esperado:
- Código HTTP 404 Not Found
- error.error_code: RESERVA_NOT_FOUND

### ❌ Caso 5: Reserva ya fue procesada

- Precondición: Reserva con ID 1 ya está "aprobada".
- Acción: Intentar aprobarla nuevamente con estado = "aprobada".
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: RESERVA_NO_PENDIENTE

### ❌ Caso 6: Estado inválido

- Precondición: Reserva con ID 1 está "pendiente".
- Acción: Ejecutar PATCH con estado = "cancelada".
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: ESTADO_INVALIDO

### ❌ Caso 7: Usuario no administrador

- Precondición: Usuario autenticado es residente (id_rol = 2).
- Acción: Ejecutar PATCH /api/v1/reservas/1/estado.
- Resultado esperado:
- Código HTTP 403 Forbidden
- error.error_code: ACCESO_DENEGADO

## ✅ Definición de Hecho

- Historia: [HU-010] Aprobación de reservas

## 📦 Alcance Funcional

- [ ] El endpoint GET /api/v1/reservas/pendientes está implementado.
- [ ] El endpoint PATCH /api/v1/reservas/{id}/estado está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de permisos (solo administradores) funciona.
- [ ] La validación de reserva existente funciona.
- [ ] La validación de estado pendiente funciona.
- [ ] La validación de estado válido funciona.
- [ ] Se registra la fecha de aprobación y quién aprobó.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada validación.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.

## 📄 Documentación Técnica

- [ ] Endpoints documentados en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, campos de entrada y salida.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para permisos insuficientes.
- [ ] Se devuelve código HTTP 404 para reserva no encontrada.