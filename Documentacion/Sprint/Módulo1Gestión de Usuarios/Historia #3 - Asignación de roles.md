## 📖 Historia de Usuario

Como administrador principal del conjunto

Quiero que el sistema me permita asignar roles específicos como administrador, residente o vigilante a cada usuario registrado, definiendo automáticamente los permisos de cada rol

Para controlar quién puede realizar acciones administrativas como aprobar reservas o generar reportes, y quién solo puede consultar información o hacer solicitudes

## 🔁 Flujo Esperado (Backend)
- Se recibe una petición PATCH en /api/v1/usuarios/{id}/rol con el nuevo id_rol en el cuerpo de la solicitud en formato JSON.
- Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).
- Se valida que el parámetro {id} de la URL corresponda a un usuario existente en la tabla usuarios.
- Se valida que el id_rol enviado sea válido (1: administrador, 2: residente).
- Se valida que un administrador no pueda cambiarse su propio rol.
- Se actualiza el rol del usuario en la base de datos.
- Se registra el cambio en una tabla de auditoría (auditoria_roles).
- Se retorna una respuesta JSON con código 200 OK y los datos actualizados del usuario.

## ✅ Criterios de Aceptación
## 1. 🔍 Estructura y lógica del servicio
- [ ] Se expone un endpoint PATCH /api/v1/usuarios/{id}/rol para asignación de roles.
- [ ] Se valida que el usuario autenticado sea administrador (id_rol = 1).
- [ ] Se valida que el usuario a modificar exista en la tabla usuarios.
- [ ] Se valida que el nuevo id_rol sea 1 (administrador) o 2 (residente).
- [ ] Se valida que un administrador no pueda cambiarse su propio rol (para evitar perder acceso).
- [ ] Se registra la auditoría del cambio de rol.

## 2. 📤 Estructura de la información
- [ ] Se responde con la siguiente estructura en JSON para asignación exitosa:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Rol actualizado exitosamente",
  "data": {
    "id_usuario": 2,
    "nombre_completo": "María López",
    "email": "maria@example.com",
    "id_rol": 1,
    "rol_nombre": "administrador",
    "actualizado_por": "Juan Pérez (ID: 1)"
  }
}

- [ ] Respuesta de error por usuario no autenticado:
{
  "success": false,
  "statusCode": 401,
  "message": "No autenticado",
  "error": {
    "error_code": "NO_AUTENTICADO",
    "details": "Se requiere un token de autenticación válido",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por permisos insuficientes:
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "ACCESO_DENEGADO",
    "details": "Se requiere rol de administrador para realizar esta acción",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por usuario no encontrado:
{
  "success": false,
  "statusCode": 404,
  "message": "Usuario no encontrado",
  "error": {
    "error_code": "USUARIO_NOT_FOUND",
    "details": "No existe un usuario con el ID 99",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por rol inválido:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "ROL_INVALIDO",
    "details": "El rol debe ser 1 (administrador) o 2 (residente)",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por auto-modificación:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "AUTO_MODIFICACION_NO_PERMITIDA",
    "details": "No puedes cambiar tu propio rol de administrador",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🔧 Notas Técnicas
## Reglas de negocio
- Solo los administradores pueden asignar o modificar roles de otros usuarios.
- Un administrador no puede cambiar su propio rol para evitar quedar sin acceso administrativo.
- El cambio de rol debe registrarse en una tabla de auditoría.

## Base de datos (tabla usuarios)
- La tabla ya existe con la columna id_rol. Se debe crear una tabla adicional de auditoría:

- Tabla auditoria_roles:

- id_auditoria: SERIAL / AUTO_INCREMENT (PK)
- id_usuario_modificado: INT, NOT NULL
- rol_anterior: INT, NOT NULL
- rol_nuevo: INT, NOT NULL
- id_usuario_modificador: INT, NOT NULL
- fecha_modificacion: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
- ip_origen: VARCHAR(45), NULLABLE

## Seguridad
- Validar el token JWT antes de procesar la solicitud.
- Extraer el id_usuario del token para identificar quién realiza la acción.
- Verificar que id_rol del token sea 1 (administrador).
- No permitir que id_usuario del token sea igual al id de la URL (auto-modificación).

## Manejo de errores
- Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, USUARIO_NOT_FOUND, ROL_INVALIDO, AUTO_MODIFICACION_NO_PERMITIDA) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Asignación de roles
- Método HTTP: PATCH
- Ruta: /api/v1/usuarios/{id}/rol
- Autenticación requerida: Sí (solo administradores)

# 📤 Ejemplo de Request
- URL: PATCH /api/v1/usuarios/2/rol
- Request Body:
{
  "id_rol": 1
}

## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
{
  "success": true,
  "statusCode": 200,
  "message": "Rol actualizado exitosamente",
  "data": {
    "id_usuario": 2,
    "nombre_completo": "María López",
    "email": "maria@example.com",
    "id_rol": 1,
    "rol_nombre": "administrador",
    "actualizado_por": "Juan Pérez (ID: 1)"
  }
}

## 📤 Ejemplo de Respuesta JSON Error (403 Forbidden)
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "ACCESO_DENEGADO",
    "details": "Se requiere rol de administrador para realizar esta acción",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
## ✅ Caso 1: Asignación exitosa de rol a otro usuario
- Precondición: Usuario autenticado es administrador (id_rol = 1). Existe un usuario con ID 2.
- Acción: Ejecutar PATCH /api/v1/usuarios/2/rol con id_rol = 1.
- Resultado esperado:
- Código HTTP 200 OK
- success: true
- El rol del usuario con ID 2 cambia a administrador
- Se registra un registro en la tabla auditoria_roles

## ❌ Caso 2: Usuario autenticado no es administrador
- Precondición: Usuario autenticado es residente (id_rol = 2).
- Acción: Ejecutar PATCH /api/v1/usuarios/2/rol con id_rol = 1.
- Resultado esperado:
- Código HTTP 403 Forbidden
- success: false
- error.error_code: ACCESO_DENEGADO
- El rol del usuario no se modifica

## ❌ Caso 3: Usuario a modificar no existe
- Precondición: Usuario autenticado es administrador. El usuario con ID 99 no existe.
- Acción: Ejecutar PATCH /api/v1/usuarios/99/rol con id_rol = 1.
- Resultado esperado:
- Código HTTP 404 Not Found
- success: false
- error.error_code: USUARIO_NOT_FOUND

## ❌ Caso 4: Rol inválido
- Precondición: Usuario autenticado es administrador. Existe usuario con ID 2.
- Acción: Ejecutar PATCH /api/v1/usuarios/2/rol con id_rol = 99.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: ROL_INVALIDO

## ❌ Caso 5: Administrador intenta cambiar su propio rol
- Precondición: Usuario autenticado es administrador con ID 1.
- Acción: Ejecutar PATCH /api/v1/usuarios/1/rol con id_rol = 2.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: AUTO_MODIFICACION_NO_PERMITIDA
- El rol del administrador no se modifica

## ❌ Caso 6: Usuario no autenticado
- Precondición: El cliente no envía token de autenticación.
- Acción: Ejecutar PATCH /api/v1/usuarios/2/rol sin el header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: NO_AUTENTICADO

## ✅ Caso 7: Verificar auditoría del cambio
- Precondición: Usuario autenticado es administrador. Existe usuario con ID 2.
- Acción: Ejecutar PATCH /api/v1/usuarios/2/rol con id_rol = 2.
- Resultado esperado:
- La tabla auditoria_roles tiene un nuevo registro con:
- id_usuario_modificado = 2
- rol_anterior (el valor antes del cambio)
- rol_nuevo = 2
- id_usuario_modificador (ID del administrador)
- fecha_modificacion con la fecha y hora actual

## ✅ Definición de Hecho
- Historia: [HU-003] Asignación de roles
## 📦 Alcance Funcional
- [ ] El endpoint PATCH /api/v1/usuarios/{id}/rol está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de permisos (solo administradores) funciona.
- [ ] La validación de usuario existente funciona.
- [ ] La validación de rol válido funciona.
- [ ] La validación de auto-modificación funciona.
- [ ] La auditoría del cambio de rol se registra correctamente.
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
- [ ] Se devuelve código HTTP 404 para usuario no encontrado.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.
- [ ] No se devuelve información sensible en los errores.