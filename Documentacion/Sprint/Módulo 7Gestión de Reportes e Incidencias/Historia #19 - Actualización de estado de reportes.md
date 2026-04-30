## 📖 Historia de Usuario

Como administrador del conjunto

Quiero que el sistema me permita cambiar el estado de un reporte a "en proceso" o "resuelto", agregar observaciones y asignar un responsable

Para mantener informado al residente sobre el avance de su reporte y garantizar que sea atendido por la persona indicada

## 🔁 Flujo Esperado

- Se recibe una petición PATCH en /api/v1/reportes/{id}/estado con el nuevo estado y datos adicionales en el cuerpo de la solicitud en formato JSON.
- Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).
- Se valida que el reporte exista en la tabla reportes.
- Se valida que el nuevo estado sea válido ("en_proceso" o "resuelto").
- Se valida que el responsable asignado (si se envía) exista en la tabla usuarios.
- Se actualiza el estado del reporte en la base de datos.
- Si el estado es "resuelto", se registra la fecha de resolución.
- Se actualiza el responsable asignado si se envió.
- Se guardan las observaciones del administrador.
- Se retorna una respuesta JSON con código 200 OK y los datos actualizados del reporte.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint PATCH /api/v1/reportes/{id}/estado para actualizar estado de reportes.
- [ ] Se valida que el usuario autenticado sea administrador (id_rol = 1).
- [ ] Se valida que el reporte exista.
- [ ] Se valida que el nuevo estado sea "en_proceso" o "resuelto".
- [ ] Se valida que el responsable exista (si se envía).
- [ ] Se registra la fecha de resolución cuando el estado cambia a "resuelto".

### 2. 📤 Estructura de la información

- [ ] Respuesta de actualización exitosa:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Estado del reporte actualizado exitosamente",
  "data": {
    "id_reporte": 1,
    "estado": "en_proceso",
    "observaciones": "Se asignó al personal de mantenimiento",
    "responsable": {
      "id_responsable": 3,
      "nombre": "Pedro Gómez",
      "cargo": "Mantenimiento"
    },
    "fecha_actualizacion": "2026-04-29T10:30:00Z",
    "fecha_resolucion": null
  }
}
```
- [ ] Respuesta cuando se resuelve el reporte:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Reporte resuelto exitosamente",
  "data": {
    "id_reporte": 1,
    "estado": "resuelto",
    "observaciones": "Se reemplazó el bombillo",
    "responsable": {
      "id_responsable": 3,
      "nombre": "Pedro Gómez",
      "cargo": "Mantenimiento"
    },
    "fecha_actualizacion": "2026-04-29T10:30:00Z",
    "fecha_resolucion": "2026-04-29T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por estado inválido:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "ESTADO_INVALIDO",
    "details": "El estado debe ser: en_proceso o resuelto",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por reporte no encontrado:
```json
{
  "success": false,
  "statusCode": 404,
  "message": "Reporte no encontrado",
  "error": {
    "error_code": "REPORTE_NOT_FOUND",
    "details": "No existe un reporte con el ID 99",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
## 🔧 Notas Técnicas

## Reglas de negocio

- Solo los administradores pueden actualizar el estado de los reportes.
- El flujo de estados permitido es: "pendiente" → "en_proceso" → "resuelto".
- No se puede volver a un estado anterior (ej: de "resuelto" a "en_proceso").
- Al cambiar a "resuelto", se asigna automáticamente la fecha de resolución.
- Las observaciones son opcionales pero recomendadas.

## Base de datos (tabla reportes)

La tabla debe incluir las siguientes columnas adicionales:

- observaciones: TEXT
- fecha_actualizacion: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE
- fecha_resolucion: TIMESTAMP, NULLABLE

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- Verificar que el usuario tenga rol de administrador (id_rol = 1).

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, REPORTE_NOT_FOUND, ESTADO_INVALIDO, RESPONSABLE_NOT_FOUND) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Actualización de estado de reportes

- Método HTTP: PATCH
- Ruta: /api/v1/reportes/{id}/estado
- Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Request

- URL: PATCH /api/v1/reportes/1/estado
- Request Body:
```json
{
  "estado": "en_proceso",
  "observaciones": "Se asignó al personal de mantenimiento",
  "id_responsable": 3
}
```
## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Estado del reporte actualizado exitosamente",
  "data": {
    "id_reporte": 1,
    "estado": "en_proceso",
    "observaciones": "Se asignó al personal de mantenimiento",
    "responsable": {
      "id_responsable": 3,
      "nombre": "Pedro Gómez",
      "cargo": "Mantenimiento"
    },
    "fecha_actualizacion": "2026-04-29T10:30:00Z",
    "fecha_resolucion": null
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
    "details": "Se requiere rol de administrador para actualizar el estado de reportes",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Cambiar estado a "en_proceso"

- Precondición: Usuario autenticado es administrador. Reporte con ID 1 está "pendiente".
- Acción: Enviar PATCH /api/v1/reportes/1/estado con estado = "en_proceso".
- Resultado esperado:
- Código HTTP 200 OK
- data.estado = "en_proceso"
- fecha_resolucion = null

### ✅ Caso 2: Cambiar estado a "resuelto"

- Precondición: Usuario autenticado es administrador. Reporte con ID 1 está "en_proceso".
- Acción: Enviar PATCH /api/v1/reportes/1/estado con estado = "resuelto".
- Resultado esperado:
- Código HTTP 200 OK
- data.estado = "resuelto"
- fecha_resolucion se asigna automáticamente

### ✅ Caso 3: Asignar responsable

- Precondición: Usuario autenticado es administrador. Reporte con ID 1 existe. Usuario ID 3 existe.
- Acción: Enviar PATCH /api/v1/reportes/1/estado con id_responsable = 3.
- Resultado esperado:
- data.responsable.id_responsable = 3
- El responsable se guarda en la base de datos

### ❌ Caso 4: Estado inválido

- Precondición: Usuario autenticado es administrador.
- Acción: Enviar PATCH /api/v1/reportes/1/estado con estado = "cancelado".
- Resultado esperado:
- Código HTTP 400 Bad Request
- error.error_code: ESTADO_INVALIDO

### ❌ Caso 5: Reporte no existe

- Precondición: Usuario autenticado es administrador. No existe reporte con ID 99.
- Acción: Enviar PATCH /api/v1/reportes/99/estado.
- Resultado esperado:
- Código HTTP 404 Not Found
- error.error_code: REPORTE_NOT_FOUND

### ❌ Caso 6: Responsable no existe

- Precondición: Usuario autenticado es administrador. Reporte con ID 1 existe. No existe usuario con ID 99.
- Acción: Enviar PATCH /api/v1/reportes/1/estado con id_responsable = 99.
- Resultado esperado:
- Código HTTP 404 Not Found
- error.error_code: RESPONSABLE_NOT_FOUND

### ❌ Caso 7: Usuario no autenticado

- Precondición: El cliente no envía token de autenticación.
- Acción: Enviar PATCH /api/v1/reportes/1/estado sin header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- error.error_code: NO_AUTENTICADO

### ❌ Caso 8: Usuario autenticado no es administrador

- Precondición: Usuario autenticado es residente (id_rol = 2).
- Acción: Enviar PATCH /api/v1/reportes/1/estado con token de residente.
- Resultado esperado:
- Código HTTP 403 Forbidden
- error.error_code: ACCESO_DENEGADO

## ✅ Definición de Hecho

- Historia: [HU-019] Actualización de estado de reportes

## 📦 Alcance Funcional

- [ ] El endpoint PATCH /api/v1/reportes/{id}/estado está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de permisos (solo administradores) funciona.
- [ ] La validación de reporte existente funciona.
- [ ] La validación de estado válido funciona.
- [ ] La asignación de responsable funciona.
- [ ] La fecha de resolución se asigna automáticamente al resolver.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada validación.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, campos de entrada y salida.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para permisos insuficientes.
- [ ] Se devuelve código HTTP 404 para recurso no encontrado.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.