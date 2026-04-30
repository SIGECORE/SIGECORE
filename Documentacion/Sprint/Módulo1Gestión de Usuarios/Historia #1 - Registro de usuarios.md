### 📖 Historia de Usuario
Como administrador del conjunto residencial

Quiero que el sistema me permita registrar nuevos residentes ingresando sus datos personales como nombre completo, correo electrónico, número de teléfono y el rol que tendrán dentro de la plataforma

Para que los residentes puedan acceder al sistema con sus propias credenciales y hacer uso de los servicios disponibles como reservas, pagos y reportes

### 🔁 Flujo Esperado

- Se recibe una petición POST en /api/v1/usuarios con los datos del nuevo usuario en el cuerpo de la solicitud en formato JSON.
- Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).
- Se valida que todos los campos requeridos (nombre_completo, email, telefono, password, id_rol) estén presentes.
- Se valida que el correo electrónico tenga formato válido.
- Se valida que el correo electrónico no esté previamente registrado en la tabla usuarios.
- Se valida que la contraseña cumpla los requisitos de seguridad (mínimo 6 caracteres).
- Se valida que el id_rol sea válido (1: administrador, 2: residente).
- Se encripta la contraseña usando bcrypt.
- Se inserta un nuevo registro en la tabla usuarios con activo = true y fecha_registro actual.
- Se retorna una respuesta JSON con código 201 Created y los datos del usuario creado (sin incluir la contraseña).

### ✅ Criterios de Aceptación

## 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST /api/v1/usuarios para registro de usuarios.
- [ ] Se valida que los campos nombre_completo, email, telefono, password e id_rol sean obligatorios.
- [ ] Se valida que el email tenga formato válido (usuario@dominio.com).
- [ ] Se valida que el email no exista previamente en la tabla usuarios.
- [ ] El campo password debe tener mínimo 6 caracteres.
- [ ] Se valida que id_rol sea 1 (administrador) o 2 (residente).
- [ ] La contraseña se encripta con bcrypt antes de guardarse.
- [ ] No se devuelve la contraseña en la respuesta.

## 2. 📤 Estructura de la información
- [ ] Se responde con la siguiente estructura en JSON para registro exitoso:
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Usuario creado exitosamente",
  "data": {
    "id_usuario": 1,
    "nombre_completo": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "3001234567",
    "id_rol": 2,
    "rol_nombre": "residente",
    "activo": true,
    "fecha_registro": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por email duplicado:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "EMAIL_DUPLICADO",
    "details": "El email juan@example.com ya está registrado",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por formato inválido:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "INVALID_DATA",
    "details": "La contraseña debe tener mínimo 6 caracteres",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por rol inválido:
```json
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
```
## 🔧 Notas Técnicas
## Reglas de negocio
- Solo los administradores pueden registrar nuevos usuarios.
- Por defecto, al registrar un usuario, el estado se establece como activo = true.
- El email se normaliza a minúsculas antes de guardarlo y antes de buscar duplicados.

## Base de datos (tabla usuarios)
- La tabla debe incluir las siguientes columnas:
- id_usuario: SERIAL / AUTO_INCREMENT (PK)
- nombre_completo: VARCHAR(100), NOT NULL
- email: VARCHAR(100), UNIQUE, NOT NULL
- telefono: VARCHAR(20), NOT NULL
- password_hash: VARCHAR(255), NOT NULL
- id_rol: INT, NOT NULL (1: administrador, 2: residente)
- activo: BOOLEAN, DEFAULT TRUE
- fecha_registro: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
- intentos_fallidos: INT, DEFAULT 0
- bloqueado_hasta: TIMESTAMP, NULLABLE

## Seguridad
- Usar la librería bcrypt con saltRounds = 10 para encriptar la contraseña.
- Normalizar el email a minúsculas antes de guardarlo y antes de buscar duplicados.
- Nunca devolver el campo password_hash en la respuesta.

## Manejo de errores
- Los códigos de error (EMAIL_DUPLICADO, INVALID_DATA, ROL_INVALIDO, CAMPO_REQUERIDO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta del Último Cierre
- Método HTTP: POST
- Ruta: /api/v1/usuarios
- Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Respuesta JSON
```json
{
  "nombre_completo": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "3001234567",
  "password": "123456",
  "id_rol": 2
}
```
## 📤 Ejemplo de Respuesta JSON Exitosa (201 Created)
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Usuario creado exitosamente",
  "data": {
    "id_usuario": 1,
    "nombre_completo": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "3001234567",
    "id_rol": 2,
    "rol_nombre": "residente",
    "activo": true,
    "fecha_registro": "2026-04-28T10:30:00Z"
  }
}
```
## 📤 Ejemplo de Respuesta JSON Error (400 Bad Request)
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "EMAIL_DUPLICADO",
    "details": "El email juan@example.com ya está registrado",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
## ✅ Caso 1: Registro exitoso con todos los campos válidos
- Precondición: El email juan@example.com no existe en la tabla usuarios. El usuario autenticado es administrador.
- Acción: Ejecutar POST /api/v1/usuarios con el JSON de ejemplo.
- Resultado esperado:
- Código HTTP 201 Created
- success: true
- statusCode: 201
- message: "Usuario creado exitosamente"
- El campo data.id_usuario contiene un número
- La contraseña almacenada en la base de datos es un hash de bcrypt, no texto plano

## ❌ Caso 2: Validación de email duplicado
- Precondición: El email juan@example.com ya existe en la base de datos.
- Acción: Enviar POST /api/v1/usuarios con el mismo email.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: EMAIL_DUPLICADO
- No se crea un nuevo usuario en la base de datos

## ❌ Caso 3: Contraseña muy corta
- Precondición: Ninguna.
- Acción: Enviar POST /api/v1/usuarios con password: "123".
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: INVALID_DATA
- error.details: "La contraseña debe tener mínimo 6 caracteres"

## ❌ Caso 4: Rol inválido
- Precondición: Ninguna.
- Acción: Enviar POST /api/v1/usuarios con id_rol: 99.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: ROL_INVALIDO
- error.details: "El rol debe ser 1 (administrador) o 2 (residente)"

## ❌ Caso 5: Formato de email inválido
- Precondición: Ninguna.
- Acción: Enviar POST /api/v1/usuarios con email: "juanexample.com".
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: INVALID_DATA
- error.details: "El email no tiene un formato válido"

## ❌ Caso 6: Campo obligatorio faltante

- Precondición: Ninguna.
- Acción: Enviar POST /api/v1/usuarios sin el campo telefono.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: CAMPO_REQUERIDO
- error.details: "El campo telefono es obligatorio"

## ✅ Caso 7: Verificar encriptación de contraseña
- Precondición: Registro exitoso.
- Acción: Consultar el usuario en la base de datos por su email.
- Resultado esperado:
- La columna password_hash contiene un hash de bcrypt (empieza con $2b$10$)
- El texto plano de la contraseña NO se encuentra en la base de datos

## ❌ Caso 8: Usuario no autenticado
- Precondición: El cliente no envía token de autenticación.
- Acción: Enviar POST /api/v1/usuarios sin el header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: NO_AUTENTICADO

## ❌ Caso 9: Usuario autenticado no es administrador
- Precondición: El token pertenece a un usuario con id_rol = 2 (residente).
- Acción: Enviar POST /api/v1/usuarios con el token de residente.
- Resultado esperado:
- Código HTTP 403 Forbidden
- success: false
- error.error_code: ACCESO_DENEGADO
- error.details: "Se requiere rol de administrador"

## ✅ Definición de Hecho
- Historia: [HU-001] Registro de usuarios
## 📦 Alcance Funcional
- [ ] El endpoint POST /api/v1/usuarios está implementado.
- [ ] Las validaciones de formato funcionan correctamente (email, contraseña, teléfono).
- [ ] La validación de unicidad de email funciona.
- [ ] La validación de rol válido funciona.
- [ ] La validación de autenticación y permisos funciona (solo administradores).
- [ ] La contraseña se encripta con bcrypt antes de guardarse.
- [ ] Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada validación.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.
- [ ] Se verificó que no se guardan contraseñas en texto plano.
- [ ] Se probaron los casos de autenticación y permisos.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, campos de entrada y salida.
- [ ] Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para permisos insuficientes.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.
- [ ] No se devuelve información sensible en los errores.