## 📖 Historia de Usuario

Como administrador del conjunto

Quiero que el sistema me permita seleccionar un usuario registrado previamente y vincularlo como propietario de un inmueble específico

Para saber quién es el responsable del pago de cuotas de administración y las obligaciones del inmueble

## 🔁 Flujo Esperado

- Se recibe una petición PATCH en /api/v1/inmuebles/{id}/propietario con el id_propietario en el cuerpo de la solicitud en formato JSON.
- Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).
- Se valida que el parámetro {id} de la URL corresponda a un inmueble existente en la tabla inmuebles.
- Se valida que el id_propietario exista en la tabla usuarios y que el usuario esté activo.
- Se valida que el inmueble no tenga ya un propietario activo.
- Se actualiza el campo id_propietario en la tabla inmuebles.
- Se cambia el estado del inmueble de "disponible" a "ocupado".
- Se registra la asignación en una tabla de auditoría (auditoria_inmuebles).
- Se retorna una respuesta JSON con código 200 OK y los datos actualizados del inmueble.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint PATCH /api/v1/inmuebles/{id}/propietario para asignación de propietario.
- [ ] Se valida que el usuario autenticado sea administrador (id_rol = 1).
- [ ] Se valida que el inmueble exista en la tabla inmuebles.
- [ ] Se valida que el propietario exista en la tabla usuarios y esté activo.
- [ ] Se valida que el inmueble no tenga ya un propietario activo.
- [ ] Se actualiza el campo id_propietario y estado del inmueble.

### 2. 📆 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON para asignación exitosa:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Propietario asignado exitosamente",
  "data": {
    "id_inmueble": 1,
    "numero": "101",
    "torre": "A",
    "area_m2": 75.5,
    "estado": "ocupado",
    "propietario": {
      "id_propietario": 5,
      "nombre_completo": "Carlos Rodríguez",
      "email": "carlos@example.com",
      "telefono": "3009876543"
    }
  }
}
```
- [ ] Respuesta de error por inmueble no encontrado:
```json
{
  "success": false,
  "statusCode": 404,
  "message": "Inmueble no encontrado",
  "error": {
    "error_code": "INMUEBLE_NOT_FOUND",
    "details": "No existe un inmueble con el ID 99",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por propietario no encontrado:
```json
{
  "success": false,
  "statusCode": 404,
  "message": "Propietario no encontrado",
  "error": {
    "error_code": "PROPIETARIO_NOT_FOUND",
    "details": "No existe un usuario con el ID 99 o el usuario está inactivo",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por inmueble ya tiene propietario:
```
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "INMUEBLE_OCUPADO",
    "details": "El inmueble ya tiene un propietario asignado. Si desea cambiar, primero debe desocuparlo",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
## 🔧 Notas Técnicas

## Reglas de negocio

- Solo los administradores pueden asignar propietarios a los inmuebles.
- Un inmueble solo puede tener un propietario activo a la vez.
- Al asignar un propietario, el estado del inmueble cambia automáticamente a "ocupado".
- Solo usuarios activos (activo = true) pueden ser asignados como propietarios.

## Base de datos (tabla inmuebles)

- La tabla inmuebles debe incluir las siguientes columnas:

- id_inmueble: SERIAL / AUTO_INCREMENT (PK)
- numero: VARCHAR(10), NOT NULL
- torre: VARCHAR(10), NOT NULL
- area_m2: DECIMAL(10,2), NOT NULL
- estado: ENUM('disponible', 'ocupado', 'mantenimiento'), DEFAULT 'disponible'
- id_propietario: INT, NULLABLE (FK referenciando usuarios.id_usuario)
- fecha_registro: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

- Tabla auditoria_inmuebles (para registrar cambios de propietario):

- id_auditoria: SERIAL / AUTO_INCREMENT (PK)
- id_inmueble: INT, NOT NULL
- id_propietario_anterior: INT, NULLABLE
- id_propietario_nuevo: INT, NOT NULL
- id_usuario_modificador: INT, NOT NULL
- fecha_modificacion: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- Verificar que id_rol del token sea 1 (administrador).
- Validar que el propietario asignado sea un usuario activo.

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, INMUEBLE_NOT_FOUND, PROPIETARIO_NOT_FOUND, INMUEBLE_OCUPADO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta del Último Cierre

- Método HTTP: PATCH
- Ruta: /api/v1/inmuebles/{id}/propietario
- Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Respuesta JSON

- URL: PATCH /api/v1/inmuebles/1/propietario
- Request Body:
```json
{
  "id_propietario": 5
}
```
## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Propietario asignado exitosamente",
  "data": {
    "id_inmueble": 1,
    "numero": "101",
    "torre": "A",
    "area_m2": 75.5,
    "estado": "ocupado",
    "propietario": {
      "id_propietario": 5,
      "nombre_completo": "Carlos Rodríguez",
      "email": "carlos@example.com",
      "telefono": "3009876543"
    }
  }
}
```
## 📤 Ejemplo de Respuesta JSON Error (404 Not Found)
```json
{
  "success": false,
  "statusCode": 404,
  "message": "Inmueble no encontrado",
  "error": {
    "error_code": "INMUEBLE_NOT_FOUND",
    "details": "No existe un inmueble con el ID 99",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Asignación exitosa de propietario

- Precondición: Usuario autenticado es administrador. Inmueble con ID 1 está disponible (estado = "disponible"). Usuario con ID 5 existe y está activo.
- Acción: Ejecutar PATCH /api/v1/inmuebles/1/propietario con id_propietario = 5.
- Resultado esperado:
- Código HTTP 200 OK
- success: true
- data.estado = "ocupado"
- data.propietario.id_propietario = 5
- Se registra un registro en la tabla auditoria_inmuebles

### ❌ Caso 2: Inmueble no existe

- Precondición: Usuario autenticado es administrador. No existe inmueble con ID 99.
- Acción: Ejecutar PATCH /api/v1/inmuebles/99/propietario con id_propietario = 5.
- Resultado esperado:
- Código HTTP 404 Not Found
- success: false
- error.error_code: INMUEBLE_NOT_FOUND

### ❌ Caso 3: Propietario no existe

- Precondición: Usuario autenticado es administrador. Inmueble con ID 1 existe. No existe usuario con ID 99.
- Acción: Ejecutar PATCH /api/v1/inmuebles/1/propietario con id_propietario = 99.
- Resultado esperado:
- Código HTTP 404 Not Found
- success: false
- error.error_code: PROPIETARIO_NOT_FOUND

### ❌ Caso 4: Propietario inactivo

- Precondición: Usuario autenticado es administrador. Inmueble con ID 1 existe. Usuario con ID 5 existe pero tiene activo = false.
- Acción: Ejecutar PATCH /api/v1/inmuebles/1/propietario con id_propietario = 5.
- Resultado esperado:
- Código HTTP 404 Not Found
- success: false
- error.error_code: PROPIETARIO_NOT_FOUND

### ❌ Caso 5: Inmueble ya tiene propietario

- Precondición: Usuario autenticado es administrador. Inmueble con ID 1 ya tiene un propietario asignado (estado = "ocupado").
- Acción: Ejecutar PATCH /api/v1/inmuebles/1/propietario con id_propietario = 5.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: INMUEBLE_OCUPADO

### ❌ Caso 6: Usuario no autenticado

- Precondición: El cliente no envía token de autenticación.
- Acción: Ejecutar PATCH /api/v1/inmuebles/1/propietario sin header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: NO_AUTENTICADO

### ❌ Caso 7: Usuario autenticado no es administrador

- Precondición: El token pertenece a un usuario con id_rol = 2 (residente).
- Acción: Ejecutar PATCH /api/v1/inmuebles/1/propietario con token de residente.
- Resultado esperado:
- Código HTTP 403 Forbidden
- success: false
- error.error_code: ACCESO_DENEGADO

### ✅ Caso 8: Verificar cambio de estado automático

- Precondición: Usuario autenticado es administrador. Inmueble con ID 1 está "disponible".
- Acción: Asignar propietario exitosamente.
- Resultado esperado:
- El campo estado del inmueble cambia a "ocupado"
- El campo id_propietario se actualiza con el ID del usuario

## ✅ Definición de Hecho

- Historia: [HU-005] Asignación de propietario a inmueble

## 📦 Alcance Funcional

- [ ] El endpoint PATCH /api/v1/inmuebles/{id}/propietario está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de permisos (solo administradores) funciona.
- [ ] La validación de inmueble existente funciona.
- [ ] La validación de propietario existente y activo funciona.
- [ ] La validación de inmueble sin propietario funciona.
- [ ] El estado del inmueble cambia a "ocupado" automáticamente.
- [ ] La auditoría de la asignación se registra correctamente.
- [ ] Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada validación.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.
- [ ] Se verificó el registro de auditoría.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, campos de entrada y salida.
- [ ] Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para permisos insuficientes.
- [ ] Se devuelve código HTTP 404 para recursos no encontrados.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.