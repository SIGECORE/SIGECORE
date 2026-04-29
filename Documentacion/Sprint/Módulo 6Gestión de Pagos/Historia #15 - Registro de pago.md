## 📖 Historia de Usuario
Como residente del conjunto

Quiero que el sistema me permita realizar el pago de mi cuota de administración a través de una pasarela de pagos integrada, seleccionando el método de pago entre tarjeta de crédito, débito o transferencia

Para evitar desplazarme a pagar en efectivo y tener un comprobante digital inmediato de mi transacción

## 🔁 Flujo Esperado
Se recibe una petición POST en /api/v1/pagos con los datos del pago en el cuerpo de la solicitud en formato JSON.

Se valida que el usuario esté autenticado.

Se valida que los campos requeridos (id_inmueble, monto, metodo_pago) estén presentes.

Se valida que monto sea un número mayor a 0.

Se valida que id_inmueble exista en la tabla inmuebles.

Se valida que el usuario autenticado sea el propietario del inmueble o un administrador.

Se procesa el pago a través de la pasarela de pagos externa.

Si el pago es exitoso, se guarda el registro en la tabla pagos con estado "confirmado".

Se genera un comprobante de pago (recibo) y se guarda su ruta.

Se retorna una respuesta JSON con código 201 Created y los datos del pago registrado.

## ✅ Criterios de Aceptación
### 1. 🔍 Estructura y lógica del servicio
Se expone un endpoint POST /api/v1/pagos para registrar pagos.

Se valida que el usuario esté autenticado.

Se valida que los campos id_inmueble, monto, metodo_pago sean obligatorios.

Se valida que monto sea mayor a 0.

Se valida que el inmueble exista.

Se valida que el usuario sea propietario del inmueble o administrador.

Se integra con pasarela de pagos externa.

Se guarda el comprobante del pago.

### 2. 📤 Estructura de la información
Respuesta de pago exitoso:
{
  "success": true,
  "statusCode": 201,
  "message": "Pago registrado exitosamente",
  "data": {
    "id_pago": 1,
    "id_usuario": 5,
    "id_inmueble": 1,
    "monto": 150000.00,
    "metodo_pago": "tarjeta_credito",
    "estado": "confirmado",
    "fecha_pago": "2026-04-29T10:30:00Z",
    "comprobante_url": "/uploads/comprobantes/recibo_1.pdf"
  }
}
## Respuesta de error por monto inválido:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "MONTO_INVALIDO",
    "details": "El monto debe ser mayor a 0",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
## Respuesta de error por inmueble no encontrado:
{
  "success": false,
  "statusCode": 404,
  "message": "Inmueble no encontrado",
  "error": {
    "error_code": "INMUEBLE_NOT_FOUND",
    "details": "No existe un inmueble con el ID 99",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
## Respuesta de error por usuario no autorizado:
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "NO_AUTORIZADO",
    "details": "No es propietario del inmueble asociado al pago",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
## Respuesta de error por pasarela de pagos:
{
  "success": false,
  "statusCode": 502,
  "message": "Error en el procesamiento del pago",
  "error": {
    "error_code": "PASARELA_ERROR",
    "details": "La pasarela de pagos no está disponible en este momento",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
## 🔧 Notas Técnicas
Reglas de negocio
Un residente solo puede pagar la cuota de su propio inmueble.

Un administrador puede registrar pagos de cualquier inmueble.

El pago debe procesarse a través de una pasarela externa antes de registrarse.

Una vez confirmado, el pago no puede modificarse.

## Base de datos (tabla pagos)
La tabla debe incluir las siguientes columnas:

id_pago: SERIAL / AUTO_INCREMENT (PK)

id_usuario: INT, NOT NULL (FK usuarios.id_usuario)

id_inmueble: INT, NOT NULL (FK inmuebles.id_inmueble)

monto: DECIMAL(10,2), NOT NULL

metodo_pago: VARCHAR(50), NOT NULL

estado: ENUM('confirmado', 'rechazado', 'pendiente'), DEFAULT 'pendiente'

fecha_pago: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

comprobante_url: VARCHAR(255)

referencia_externa: VARCHAR(100)

## Seguridad
Validar el token JWT antes de procesar la solicitud.

Verificar que el usuario sea propietario del inmueble o administrador.

No almacenar información sensible de tarjetas de crédito.

## Manejo de errores
Los códigos de error (NO_AUTENTICADO, INMUEBLE_NOT_FOUND, MONTO_INVALIDO, NO_AUTORIZADO, PASARELA_ERROR, CAMPO_REQUERIDO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Registro de pago
Método HTTP: POST

Ruta: /api/v1/pagos

Autenticación requerida: Sí (residente propietario o administrador)

### 📤 Ejemplo de Request JSON
{
  "id_inmueble": 1,
  "monto": 150000.00,
  "metodo_pago": "tarjeta_credito",
  "token_pasarela": "tok_visa_1234"
}
### 📤 Ejemplo de Respuesta JSON Exitosa (201 Created)
{
  "success": true,
  "statusCode": 201,
  "message": "Pago registrado exitosamente",
  "data": {
    "id_pago": 1,
    "id_usuario": 5,
    "id_inmueble": 1,
    "monto": 150000.00,
    "metodo_pago": "tarjeta_credito",
    "estado": "confirmado",
    "fecha_pago": "2026-04-29T10:30:00Z",
    "comprobante_url": "/uploads/comprobantes/recibo_1.pdf"
  }
}
### 📤 Ejemplo de Respuesta JSON Error (502 Bad Gateway)
{
  "success": false,
  "statusCode": 502,
  "message": "Error en el procesamiento del pago",
  "error": {
    "error_code": "PASARELA_ERROR",
    "details": "La pasarela de pagos no está disponible en este momento",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
### ✅ Caso 1: Pago exitoso (residente propietario)
Precondición: Usuario autenticado es propietario del inmueble con ID 1. Pasarela de pagos disponible.

Acción: Enviar POST /api/v1/pagos con datos válidos.

Resultado esperado:

Código HTTP 201 Created

data.estado = "confirmado"

Se genera el comprobante de pago

### ✅ Caso 2: Administrador registra pago
Precondición: Usuario autenticado es administrador. Inmueble con ID 1 existe.

Acción: Enviar POST /api/v1/pagos para el inmueble ID 1.

Resultado esperado:

Código HTTP 201 Created

El pago se registra exitosamente

### ❌ Caso 3: Monto inválido (cero o negativo)
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/pagos con monto = 0.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: MONTO_INVALIDO

### ❌ Caso 4: Inmueble no existe
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/pagos con id_inmueble = 99.

Resultado esperado:

Código HTTP 404 Not Found

error.error_code: INMUEBLE_NOT_FOUND

### ❌ Caso 5: Residente paga inmueble que no es suyo
Precondición: Usuario autenticado es residente pero no es propietario del inmueble ID 1.

Acción: Enviar POST /api/v1/pagos con id_inmueble = 1.

Resultado esperado:

Código HTTP 403 Forbidden

error.error_code: NO_AUTORIZADO

### ❌ Caso 6: Pasarela de pagos no disponible
Precondición: La pasarela de pagos externa no responde o rechaza la transacción.

Acción: Enviar POST /api/v1/pagos con datos válidos.

Resultado esperado:

Código HTTP 502 Bad Gateway

error.error_code: PASARELA_ERROR

### ❌ Caso 7: Campo obligatorio faltante
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/pagos sin metodo_pago.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: CAMPO_REQUERIDO

### ❌ Caso 8: Usuario no autenticado
Precondición: El cliente no envía token de autenticación.

Acción: Enviar POST /api/v1/pagos sin header Authorization.

Resultado esperado:

Código HTTP 401 Unauthorized

error.error_code: NO_AUTENTICADO

## ✅ Definición de Hecho
Historia: [HU-015] Registro de pago
## 📦 Alcance Funcional
El endpoint POST /api/v1/pagos está implementado.

La validación de autenticación funciona correctamente.

La validación de campos obligatorios funciona.

La validación de monto positivo funciona.

La validación de inmueble existente funciona.

La validación de propiedad (residente) funciona.

La integración con pasarela de pagos funciona.

El comprobante de pago se genera correctamente.

## 🧪 Pruebas Completadas
Se ejecutaron pruebas unitarias para cada validación.

Se ejecutaron pruebas de integración con la pasarela de pagos.

Se probaron todos los casos de error documentados.

## 📄 Documentación Técnica
Endpoint documentado en Swagger / OpenAPI.

Se describe: propósito del endpoint, campos de entrada y salida.

## 🔐 Manejo de Errores
Se devuelve código HTTP 400 para errores de validación.

Se devuelve código HTTP 401 para usuario no autenticado.

Se devuelve código HTTP 403 para permisos insuficientes.

Se devuelve código HTTP 404 para recurso no encontrado.

Se devuelve código HTTP 502 para error de pasarela.