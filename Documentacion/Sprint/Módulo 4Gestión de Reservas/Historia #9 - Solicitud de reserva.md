## 📖 Historia de Usuario
Como administrador del conjunto

Quiero que el sistema me muestre una lista de todas las solicitudes de reserva pendientes con los datos del solicitante, la zona, la fecha y el horario solicitado, y que me permita aprobarlas o rechazarlas

Para evitar conflictos de horarios entre diferentes residentes y garantizar el uso ordenado de las zonas comunes

## 🔁 Flujo Esperado 
Se recibe una petición POST en /api/v1/reservas con los datos de la reserva en el cuerpo de la solicitud en formato JSON.

Se valida que el usuario esté autenticado.

Se valida que los campos requeridos (id_zona, fecha, hora_inicio, hora_fin) estén presentes.

Se valida que la fecha no sea anterior a la fecha actual.

Se valida que hora_inicio sea menor que hora_fin.

Se valida que la zona exista en la tabla zonas_comunes y que su estado sea "disponible".

Se verifica que no existan reservas aprobadas que solapen con el horario solicitado.

Se valida que el residente no tenga pagos pendientes (según regla de negocio).

Se guarda la reserva en la tabla reservas con estado "pendiente", fecha_solicitud actual y id_usuario obtenido del token.

Se retorna una respuesta JSON con código 201 Created y los datos de la reserva creada.

## ✅ Criterios de Aceptación
### 1. 🔍 Estructura y lógica del servicio
Se expone un endpoint POST /api/v1/reservas para solicitud de reserva.

Se valida que el usuario esté autenticado.

Se valida que la zona exista y esté disponible.

Se valida que la fecha no sea pasada.

Se valida que hora_inicio < hora_fin.

Se valida disponibilidad (sin conflictos de horario).

Se asigna estado "pendiente" a la nueva reserva.

### 2. 📤 Estructura de la información
## Se responde con la siguiente estructura en JSON para solicitud exitosa:
{
  "success": true,
  "statusCode": 201,
  "message": "Solicitud de reserva creada exitosamente, pendiente de aprobación",
  "data": {
    "id_reserva": 1,
    "id_usuario": 5,
    "nombre_usuario": "Carlos Rodríguez",
    "id_zona": 1,
    "nombre_zona": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "estado": "pendiente",
    "fecha_solicitud": "2026-04-28T10:30:00Z"
  }
}
## Respuesta de error por zona no disponible:
{
  "success": false,
  "statusCode": 409,
  "message": "Conflicto de horario",
  "error": {
    "error_code": "RESERVA_CONFLICTO",
    "details": "La zona ya está reservada en el horario solicitado",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
## Respuesta de error por morosidad:
{
  "success": false,
  "statusCode": 400,
  "message": "No se puede realizar la reserva",
  "error": {
    "error_code": "MOROSIDAD",
    "details": "El residente tiene pagos pendientes de cuotas de administración",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
## 🔧 Notas Técnicas
## Reglas de negocio
Solo residentes autenticados pueden solicitar reservas.

Un residente con pagos pendientes no puede solicitar reservas.

La selección de la zona debe validar que esté disponible.

No se pueden reservar fechas pasadas.

Una reserva no puede solapar con otra reserva aprobada.

El estado inicial de toda reserva es "pendiente".

El residente debe estar activo en el sistema.

## Base de datos (tabla reservas)
La tabla debe incluir las siguientes columnas:

id_reserva: SERIAL / AUTO_INCREMENT (PK)

id_usuario: INT, NOT NULL (FK usuarios.id_usuario)

id_zona: INT, NOT NULL (FK zonas_comunes.id_zona)

fecha: DATE, NOT NULL

hora_inicio: TIME, NOT NULL

hora_fin: TIME, NOT NULL

estado: ENUM('pendiente', 'aprobada', 'rechazada', 'cancelada'), DEFAULT 'pendiente'

observaciones: TEXT

fecha_solicitud: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

fecha_aprobacion: TIMESTAMP, NULLABLE

aprobado_por: INT, NULLABLE (FK usuarios.id_usuario)

## Seguridad
Validar el token JWT antes de procesar la solicitud.

El id_usuario se obtiene del token, no del request body.

Validar que el usuario esté activo (activo = true).

## Manejo de errores
Los códigos de error (NO_AUTENTICADO, ZONA_NOT_FOUND, ZONA_MANTENIMIENTO, FECHA_INVALIDA, HORARIO_INVALIDO, RESERVA_CONFLICTO, MOROSIDAD, USUARIO_INACTIVO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Solicitud de reserva
Método HTTP: POST

Ruta: /api/v1/reservas

Autenticación requerida: Sí (residente o administrador)

## 📤 Ejemplo de Request JSON
{
  "id_zona": 1,
  "fecha": "2026-05-15",
  "hora_inicio": "14:00",
  "hora_fin": "18:00",
  "observaciones": "Cumpleaños familiar"
}
## 📤 Ejemplo de Respuesta JSON Exitosa (201 Created)
{
  "success": true,
  "statusCode": 201,
  "message": "Solicitud de reserva creada exitosamente, pendiente de aprobación",
  "data": {
    "id_reserva": 1,
    "id_usuario": 5,
    "nombre_usuario": "Carlos Rodríguez",
    "id_zona": 1,
    "nombre_zona": "Salón Social",
    "fecha": "2026-05-15",
    "hora_inicio": "14:00",
    "hora_fin": "18:00",
    "estado": "pendiente",
    "fecha_solicitud": "2026-04-28T10:30:00Z"
  }
}
## 📤 Ejemplo de Respuesta JSON Error (409 Conflict)
{
  "success": false,
  "statusCode": 409,
  "message": "Conflicto de horario",
  "error": {
    "error_code": "RESERVA_CONFLICTO",
    "details": "La zona ya está reservada en el horario solicitado",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
### ✅ Caso 1: Solicitud exitosa de reserva
Precondición: Usuario autenticado, activo, sin morosidad. Zona existe y está disponible. No hay conflictos de horario.

Acción: Ejecutar POST /api/v1/reservas con datos válidos.

Resultado esperado:

Código HTTP 201 Created

success: true

data.estado = "pendiente"

La reserva se guarda en la base de datos

### ❌ Caso 2: Conflicto de horario
Precondición: Ya existe una reserva aprobada para la zona en el mismo horario.

Acción: Solicitar reserva para el mismo horario.

Resultado esperado:

Código HTTP 409 Conflict

error.error_code: RESERVA_CONFLICTO

### ❌ Caso 3: Zona en mantenimiento
Precondición: La zona seleccionada tiene estado "mantenimiento".

Acción: Solicitar reserva para esa zona.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: ZONA_MANTENIMIENTO

### ❌ Caso 4: Zona no existe
Precondición: No existe zona con el ID enviado.

Acción: Solicitar reserva con id_zona = 99.

Resultado esperado:

Código HTTP 404 Not Found

error.error_code: ZONA_NOT_FOUND

### ❌ Caso 5: Fecha pasada
Precondición: La fecha actual es 2026-04-28.

Acción: Solicitar reserva con fecha = 2026-04-27.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: FECHA_INVALIDA

### ❌ Caso 6: Horario inválido
Precondición: Ninguna.

Acción: Solicitar reserva con hora_inicio = 18:00 y hora_fin = 14:00.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: HORARIO_INVALIDO

### ❌ Caso 7: Residentes con morosidad
Precondición: Usuario autenticado tiene pagos pendientes de administración.

Acción: Solicitar reserva.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: MOROSIDAD

### ❌ Caso 8: Usuario inactivo
Precondición: Usuario autenticado tiene activo = false.

Acción: Solicitar reserva.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: USUARIO_INACTIVO

### ❌ Caso 9: Usuario no autenticado
Precondición: El cliente no envía token de autenticación.

Acción: Solicitar reserva sin header Authorization.

Resultado esperado:

Código HTTP 401 Unauthorized

error.error_code: NO_AUTENTICADO

## ✅ Definición de Hecho
#Historia: [HU-009] Solicitud de reserva
## 📦 Alcance Funcional
El endpoint POST /api/v1/reservas está implementado.

La validación de autenticación funciona correctamente.

La validación de zona existente y disponible funciona.

La validación de fecha no pasada funciona.

La validación de horario válido funciona.

La validación de conflicto de horario funciona.

La validación de morosidad funciona.

La validación de usuario activo funciona.

El estado inicial "pendiente" se asigna automáticamente.

Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas
Se ejecutaron pruebas unitarias para cada validación.

Se ejecutaron pruebas de integración para el flujo completo.

Se probaron todos los casos de error documentados.

Se probaron diferentes combinaciones de horarios.

## 📄 Documentación Técnica
Endpoint documentado en Swagger / OpenAPI.

Se describe: propósito del endpoint, campos de entrada y salida.

Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores
Se devuelve código HTTP 400 para errores de validación.

Se devuelve código HTTP 401 para usuario no autenticado.

Se devuelve código HTTP 404 para zona no encontrada.

Se devuelve código HTTP 409 para conflicto de horario.

El campo error en el JSON incluye error_code, details y timestamp.