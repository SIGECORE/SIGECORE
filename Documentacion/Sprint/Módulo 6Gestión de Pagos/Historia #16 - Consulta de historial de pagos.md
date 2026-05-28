## 📖 Historia de Usuario

Como residente del conjunto

Quiero que el sistema me muestre mi historial completo de pagos con las fechas, los montos pagados, el método de pago utilizado y el estado de cada transacción

Para saber si tengo cuotas pendientes y tener claridad sobre mi situación financiera con el conjunto

## 🔁 Flujo Esperado

- Se recibe una petición GET en /api/v1/pagos/usuario/{id} para consultar el historial de pagos de un usuario específico.
- Se valida que el usuario esté autenticado.
- Se valida que el {id} de la URL corresponda a un usuario existente en la tabla usuarios.
- Se valida que el usuario autenticado sea el mismo usuario de la consulta o un administrador.
- Se consulta la tabla pagos filtrando por id_usuario.
- Se ordenan los resultados por fecha_pago descendente (más recientes primero).
- Se retorna una respuesta JSON con la lista de pagos del usuario.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET /api/v1/pagos/usuario/{id} para consultar historial de pagos por usuario.
- [ ] Se valida que el usuario esté autenticado.
- [ ] Se valida que el usuario de la URL exista.
- [ ] Se valida que el usuario autenticado sea el mismo o un administrador.
- [ ] Se retornan los pagos ordenados por fecha descendente.

### 2. 📤 Estructura de la información
- [ ] Respuesta de consulta exitosa:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Consulta exitosa",
  "data": {
    "usuario": {
      "id_usuario": 5,
      "nombre_completo": "Carlos Rodríguez",
      "email": "carlos@example.com"
    },
    "pagos": [
      {
        "id_pago": 3,
        "inmueble": {
          "id_inmueble": 1,
          "numero": "101",
          "torre": "A"
        },
        "monto": 150000.00,
        "metodo_pago": "tarjeta_credito",
        "estado": "confirmado",
        "fecha_pago": "2026-04-15T10:30:00Z",
        "comprobante_url": "/uploads/comprobantes/recibo_3.pdf"
      },
      {
        "id_pago": 1,
        "inmueble": {
          "id_inmueble": 1,
          "numero": "101",
          "torre": "A"
        },
        "monto": 150000.00,
        "metodo_pago": "transferencia",
        "estado": "confirmado",
        "fecha_pago": "2026-03-15T10:30:00Z",
        "comprobante_url": "/uploads/comprobantes/recibo_1.pdf"
      }
    ]
  }
}
```
- [ ] Respuesta cuando no hay pagos registrados:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "El usuario no tiene pagos registrados",
  "data": {
    "usuario": {
      "id_usuario": 5,
      "nombre_completo": "Carlos Rodríguez"
    },
    "pagos": []
  }
}
```
- [ ] Respuesta de error por usuario no encontrado:
```json
{
  "success": false,
  "statusCode": 404,
  "message": "Usuario no encontrado",
  "error": {
    "error_code": "USUARIO_NOT_FOUND",
    "details": "No existe un usuario con el ID 99",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
## 🔧 Notas Técnicas

## Reglas de negocio

- Un residente solo puede consultar su propio historial de pagos.
- Un administrador puede consultar el historial de pagos de cualquier usuario.
- Los resultados deben mostrarse ordenados por fecha de pago descendente.
- Se debe incluir información del inmueble (número y torre) en cada pago.

## Base de datos (tablas pagos e inmuebles)

- Se debe hacer un JOIN con la tabla inmuebles para obtener el número y torre del inmueble.
- Se debe hacer un JOIN con la tabla usuarios para obtener los datos del usuario.

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- El id_usuario se obtiene del token para comparar con el {id} de la URL.
- Verificar que el usuario autenticado sea el propietario o administrador.

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, USUARIO_NOT_FOUND, ACCESO_DENEGADO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta de historial de pagos

- Método HTTP: GET
- Ruta: /api/v1/pagos/usuario/{id}
- Autenticación requerida: Sí (residente propietario o administrador)

## 📤 Ejemplo de Request

- URL: GET /api/v1/pagos/usuario/5

## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
```json
{
  "success": true,
  "statusCode": 200,
  "message": "Consulta exitosa",
  "data": {
    "usuario": {
      "id_usuario": 5,
      "nombre_completo": "Carlos Rodríguez",
      "email": "carlos@example.com"
    },
    "pagos": [
      {
        "id_pago": 3,
        "inmueble": {
          "id_inmueble": 1,
          "numero": "101",
          "torre": "A"
        },
        "monto": 150000.00,
        "metodo_pago": "tarjeta_credito",
        "estado": "confirmado",
        "fecha_pago": "2026-04-15T10:30:00Z",
        "comprobante_url": "/uploads/comprobantes/recibo_3.pdf"
      },
      {
        "id_pago": 1,
        "inmueble": {
          "id_inmueble": 1,
          "numero": "101",
          "torre": "A"
        },
        "monto": 150000.00,
        "metodo_pago": "transferencia",
        "estado": "confirmado",
        "fecha_pago": "2026-03-15T10:30:00Z",
        "comprobante_url": "/uploads/comprobantes/recibo_1.pdf"
      }
    ]
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
    "details": "No tiene permisos para consultar los pagos de otro usuario",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Residente consulta su propio historial de pagos

- Precondición: Usuario autenticado con ID 5. Existen pagos asociados al usuario ID 5.
- Acción: Ejecutar GET /api/v1/pagos/usuario/5.
- Resultado esperado:
- Código HTTP 200 OK
- data.usuario.id_usuario = 5
- data.pagos contiene los pagos del usuario

### ✅ Caso 2: Administrador consulta pagos de otro usuario

- Precondición: Usuario autenticado es administrador (id_rol = 1). Usuario ID 5 tiene pagos.
- Acción: Ejecutar GET /api/v1/pagos/usuario/5.
- Resultado esperado:
- Código HTTP 200 OK
- Se devuelven los pagos del usuario ID 5

### ✅ Caso 3: Usuario sin pagos

- Precondición: Usuario autenticado con ID 6 no tiene pagos registrados.
- Acción: Ejecutar GET /api/v1/pagos/usuario/6.
- Resultado esperado:
- Código HTTP 200 OK
- data.pagos es un array vacío
- message = "El usuario no tiene pagos registrados"

### ❌ Caso 4: Usuario no encontrado

- Precondición: No existe usuario con ID 99.
- Acción: Ejecutar GET /api/v1/pagos/usuario/99.
- Resultado esperado:
- Código HTTP 404 Not Found
- error.error_code: USUARIO_NOT_FOUND

### ❌ Caso 5: Residente intenta consultar pagos de otro residente

- Precondición: Usuario autenticado con ID 5 (residente). Usuario ID 6 (residente) tiene pagos.
- Acción: Ejecutar GET /api/v1/pagos/usuario/6.
- Resultado esperado:
- Código HTTP 403 Forbidden
- error.error_code: ACCESO_DENEGADO

### ❌ Caso 6: Usuario no autenticado

- Precondición: El cliente no envía token de autenticación.
- Acción: Ejecutar GET /api/v1/pagos/usuario/5 sin header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- error.error_code: NO_AUTENTICADO

### ✅ Caso 7: Verificar ordenamiento por fecha descendente

- Precondición: Usuario tiene pagos en diferentes fechas.
- Acción: Ejecutar GET /api/v1/pagos/usuario/5.
- Resultado esperado:
- Los pagos se muestran ordenados de la fecha más reciente a la más antigua

## ✅ Definición de Hecho

- Historia: [HU-016] Consulta de historial de pagos

## 📦 Alcance Funcional

- [ ] El endpoint GET /api/v1/pagos/usuario/{id} está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de usuario existente funciona.
- [ ] La validación de permisos (propietario o administrador) funciona.
- [ ] Se retorna la información completa de cada pago (incluyendo inmueble).
- [ ] Los resultados se ordenan correctamente por fecha descendente.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para la consulta.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, parámetros y salida.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para permisos insuficientes.
- [ ] Se devuelve código HTTP 404 para usuario no encontrado.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.