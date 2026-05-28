## 📖 Historia de Usuario
Como residente o administrador del conjunto

Quiero que el sistema valide mi correo y contraseña al intentar ingresar, y me otorgue acceso solo si mis credenciales son correctas y mi cuenta está activa

Para acceder de forma segura a las funcionalidades que me corresponden según mi rol dentro del conjunto residencial


## 🔁 Flujo Esperado
- Se recibe una petición POST en /api/v1/usuarios/login con el correo y la contraseña en el cuerpo de la solicitud en formato JSON.
- Se valida que los campos email y password estén presentes.
- Se busca el usuario por email en la tabla usuarios.
- Si el usuario no existe, se retorna error 401 Unauthorized.
- Si el usuario existe pero está inactivo (activo = false), se retorna error 401 Unauthorized.
- Si el usuario existe y está activo, se verifica la contraseña usando bcrypt.compare() contra el password_hash almacenado.
- Si la contraseña es incorrecta, se incrementa intentos_fallidos. Si supera 3 intentos, se bloquea la cuenta temporalmente.
- Si la contraseña es correcta, se resetea intentos_fallidos a 0.
- Se genera un token JWT con id_usuario, nombre_completo, email, id_rol y tiempo de expiración de 8 horas.
- Se retorna una respuesta JSON con código 200 OK con el token y los datos básicos del usuario.

## ✅ Criterios de Aceptación
### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST /api/v1/usuarios/login para inicio de sesión.
- [ ] Se valida que los campos email y password sean obligatorios.
- [ ] Se valida que el email exista en la tabla usuarios.
- [ ] Se valida que el usuario esté activo (activo = true).
- [ ] Se valida la contraseña contra el hash almacenado en la base de datos.
- [ ] Se genera un token JWT válido con expiración de 8 horas.
- [ ] Se registra el intento de login (fecha/hora) en una tabla de auditoría.

### 2. 📤 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON para login exitoso:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Inicio de sesión exitoso",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInT5cCI6IkpXVCJ9...",
    "usuario": {
      "id_usuario": 1,
      "nombre_completo": "Juan Pérez",
      "email": "juan@example.com",
      "id_rol": 2,
      "rol_nombre": "residente"
    }
  }
}
```
- [ ] Respuesta de error por credenciales incorrectas:
```json
{
  "success": false,
  "statusCode": 401,
  "message": "Credenciales inválidas",
  "error": {
    "error_code": "CREDENCIALES_INVALIDAS",
    "details": "El correo o la contraseña son incorrectos",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por usuario inactivo:
```json
{
  "success": false,
  "statusCode": 401,
  "message": "Cuenta inactiva",
  "error": {
    "error_code": "USUARIO_INACTIVO",
    "details": "La cuenta del usuario está desactivada. Contacte al administrador.",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por cuenta bloqueada:
```json
{
  "success": false,
  "statusCode": 423,
  "message": "Cuenta bloqueada",
  "error": {
    "error_code": "CUENTA_BLOQUEADA",
    "details": "Demasiados intentos fallidos. Cuenta bloqueada por 30 minutos.",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
## 🔧 Notas Técnicas
## Reglas de negocio
- Después de 3 intentos fallidos de login, la cuenta se bloquea por 30 minutos.
- El campo bloqueado_hasta se actualiza con la fecha y hora actual más 30 minutos.
- Al iniciar sesión exitosamente, el contador intentos_fallidos se resetea a 0.

## Base de datos (tabla usuarios)
- La tabla debe incluir las siguientes columnas (además de las ya definidas):
- ultimo_login: TIMESTAMP, NULLABLE
- ip_registro: VARCHAR(45), NULLABLE
- user_agent: TEXT, NULLABLE

## Seguridad
- Usar la librería bcrypt con saltRounds = 10 para verificar la contraseña.
- Usar la librería jsonwebtoken (JWT) con algoritmo HS256 y tiempo de expiración de 8 horas.
- La clave secreta del JWT debe estar en variables de entorno (.env), no en el código.
- Normalizar el email a minúsculas antes de buscar en la base de datos.
- Nunca devolver el campo password_hash en la respuesta.
- El token JWT debe incluir iat (issued at) y exp (expiration).

## Manejo de errores
- Los códigos de error (CREDENCIALES_INVALIDAS, USUARIO_INACTIVO, CUENTA_BLOQUEADA, CAMPO_REQUERIDO) deben ser constantes definidas en un archivo de errores del sistema.
- No informar si el email existe o no para evitar enumeración de usuarios (mensaje genérico "Credenciales inválidas").

## 🚀 Endpoint – Inicio de sesión
- Método HTTP: POST
- Ruta: /api/v1/usuarios/login
- Autenticación requerida: No

## 📤 Ejemplo de Request JSON
```json
{
  "email": "juan@example.com",
  "password": "123456"
}
```
## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Inicio de sesión exitoso",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInT5cCI6IkpXVCJ9.eyJpZF91c3VhcmlvIjoxLCJub21icmVfY29tcGxldG8iOiJKdWFuIFBlcmV6IiwiZW1haWwiOiJqdWFuQGV4YW1wbGUuY29tIiwiaWRfcm9sIjoyLCJpYXQiOjE3MTQzMjAwMDAsImV4cCI6MTcxNDM0ODgwMH0.xyz123",
    "usuario": {
      "id_usuario": 1,
      "nombre_completo": "Juan Pérez",
      "email": "juan@example.com",
      "id_rol": 2,
      "rol_nombre": "residente"
    }
  }
}
```
## 📤 Ejemplo de Respuesta JSON Error (401 Unauthorized)
```json
{
  "success": false,
  "statusCode": 401,
  "message": "Credenciales inválidas",
  "error": {
    "error_code": "CREDENCIALES_INVALIDAS",
    "details": "El correo o la contraseña son incorrectos",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
## ✅ Caso 1: Login exitoso con credenciales correctas
- Precondición: Usuario registrado, activo, con email juan@example.com y contraseña 123456.
- Acción: Ejecutar POST /api/v1/usuarios/login con las credenciales correctas.
- Resultado esperado:
- Código HTTP 200 OK
- success: true
- data.token contiene un JWT válido
- El JWT contiene id_usuario, nombre_completo, email, id_rol
- El campo intentos_fallidos en la base de datos se resetea a 0
- El campo ultimo_login se actualiza con la fecha y hora actual

## ❌ Caso 2: Login con contraseña incorrecta
- Precondición: Usuario registrado con email juan@example.com
- Acción: Enviar POST /api/v1/usuarios/login con contraseña incorrecta.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: CREDENCIALES_INVALIDAS
- El campo intentos_fallidos se incrementa en 1

## ❌ Caso 3: Cuenta bloqueada por múltiples intentos fallidos
- Precondición: Usuario tiene intentos_fallidos = 3
- Acción: Enviar POST /api/v1/usuarios/login con cualquier contraseña.
- Resultado esperado:
- Código HTTP 423 Locked
- success: false
- error.error_code: CUENTA_BLOQUEADA
- La cuenta permanece bloqueada por 30 minutos

## ❌ Caso 4: Usuario inactivo
- Precondición: Usuario registrado con activo = false
- Acción: Enviar POST /api/v1/usuarios/login con credenciales correctas.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: USUARIO_INACTIVO

## ❌ Caso 5: Email no registrado
- Precondición: El email no existe en la base de datos.
- Acción: Enviar POST /api/v1/usuarios/login con email no registrado.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: CREDENCIALES_INVALIDAS (mensaje genérico, no informar si el email existe)

## ❌ Caso 6: Campos obligatorios faltantes
- Precondición: Ninguna.
- Acción: Enviar POST /api/v1/usuarios/login sin el campo email.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: CAMPO_REQUERIDO

## ✅ Caso 7: Verificar que el token JWT expira
- Precondición: Login exitoso.
- Acción: Inspeccionar el token JWT recibido.
- Resultado esperado:
- El token tiene un campo exp (expiration) con valor de 8 horas después del iat
- El token es válido durante las primeras 8 horas
- Después de 8 horas, el token es rechazado por el sistema

## ✅ Definición de Hecho
- Historia: [HU-002] Inicio de sesión
## 📦 Alcance Funcional
- [ ] El endpoint POST /api/v1/usuarios/login está implementado.
- [ ] Las validaciones de campos obligatorios funcionan.
- [ ] La validación de credenciales funciona correctamente.
- [ ] La validación de usuario activo funciona.
- [ ] El bloqueo por intentos fallidos funciona correctamente.
- [ ] El token JWT se genera correctamente.
- [ ] Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas
- [ ] Se ejecutaron pruebas unitarias para la validación de credenciales.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.
- [ ] Se verificó el bloqueo de cuenta por intentos fallidos.
- [ ] Se verificó la expiración del token JWT.

## 📄 Documentación Técnica
- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, campos de entrada y salida.
- [ ] Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores
- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para credenciales inválidas.
- [ ] Se devuelve código HTTP 423 para cuenta bloqueada.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.
- [ ] No se devuelve información sensible en los errores.