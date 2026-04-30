## 📖 Historia de Usuario

Como residente del conjunto

Quiero que el sistema me permita consultar el historial completo de mis reservas, mostrando la zona, fecha, horario y el estado actual (pendiente, aprobada, rechazada o cancelada)

Para hacer seguimiento a mis solicitudes y saber si mi reserva fue confirmada

## 🔁 Flujo Esperado

- Se recibe una petición GET en /api/v1/reservas/usuario/{id} para consultar las reservas de un usuario específico.
- Se valida que el usuario esté autenticado.
- Se valida que el {id} de la URL corresponda a un usuario existente en la tabla usuarios.
- Se valida que el usuario autenticado sea el mismo usuario de la consulta o un administrador.
- Se consulta la tabla reservas filtrando por id_usuario.
- Se ordenan los resultados por fecha descendente (más recientes primero).
- Se retorna una respuesta JSON con la lista de reservas del usuario.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint GET /api/v1/reservas/usuario/{id} para consultar reservas por usuario.
- [ ] Se valida que el usuario esté autenticado.
- [ ] Se valida que el usuario de la URL exista.
- [ ] Se valida que el usuario autenticado sea el mismo o un administrador.
- [ ] Se retornan las reservas ordenadas por fecha descendente.

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
    "reservas": [
      {
        "id_reserva": 3,
        "zona": {
          "id_zona": 2,
          "nombre": "Cancha de Tenis"
        },
        "fecha": "2026-05-20",
        "hora_inicio": "15:00",
        "hora_fin": "17:00",
        "estado": "aprobada",
        "fecha_solicitud": "2026-04-25T10:30:00Z"
      },
      {
        "id_reserva": 1,
        "zona": {
          "id_zona": 1,
          "nombre": "Salón Social"
        },
        "fecha": "2026-05-15",
        "hora_inicio": "14:00",
        "hora_fin": "18:00",
        "estado": "pendiente",
        "fecha_solicitud": "2026-04-20T10:30:00Z"
      }
    ]
  }
}

- [ ] Respuesta cuando no hay reservas:
```json
{
  "success": true,
  "statusCode": 200,
  "message": "El usuario no tiene reservas registradas",
  "data": {
    "usuario": {
      "id_usuario": 5,
      "nombre_completo": "Carlos Rodríguez"
    },
    "reservas": []
  }
}

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

## 🔧 Notas Técnicas

## Reglas de negocio

- Un residente solo puede consultar sus propias reservas.
- Un administrador puede consultar las reservas de cualquier usuario.
- Los resultados deben mostrarse ordenados por fecha descendente.
- Se debe incluir información de la zona (nombre) en cada reserva.

## Base de datos (tablas reservas y zonas_comunes)

- Se debe hacer un JOIN con la tabla zonas_comunes para obtener el nombre de la zona.
- Se debe hacer un JOIN con la tabla usuarios para obtener los datos del usuario.

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- El id_usuario se obtiene del token para comparar con el {id} de la URL.
- Verificar que el usuario autenticado sea el propietario o administrador.

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, USUARIO_NOT_FOUND, ACCESO_DENEGADO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta de reservas por usuario

- Método HTTP: GET
- Ruta: /api/v1/reservas/usuario/{id}
- Autenticación requerida: Sí (residente propietario o administrador)

## 📤 Ejemplo de Request

- URL: GET /api/v1/reservas/usuario/5

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
    "reservas": [
      {
        "id_reserva": 3,
        "zona": {
          "id_zona": 2,
          "nombre": "Cancha de Tenis"
        },
        "fecha": "2026-05-20",
        "hora_inicio": "15:00",
        "hora_fin": "17:00",
        "estado": "aprobada",
        "fecha_solicitud": "2026-04-25T10:30:00Z"
      },
      {
        "id_reserva": 1,
        "zona": {
          "id_zona": 1,
          "nombre": "Salón Social"
        },
        "fecha": "2026-05-15",
        "hora_inicio": "14:00",
        "hora_fin": "18:00",
        "estado": "pendiente",
        "fecha_solicitud": "2026-04-20T10:30:00Z"
      }
    ]
  }
}

## 📤 Ejemplo de Respuesta JSON Error (403 Forbidden)
```json
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "ACCESO_DENEGADO",
    "details": "No tiene permisos para consultar las reservas de otro usuario",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Residente consulta sus propias reservas

- Precondición: Usuario autenticado con ID 5. Existen reservas asociadas al usuario ID 5.
- Acción: Ejecutar GET /api/v1/reservas/usuario/5.
- Resultado esperado:
- Código HTTP 200 OK
- data.usuario.id_usuario = 5
- data.reservas contiene las reservas del usuario

### ✅ Caso 2: Administrador consulta reservas de otro usuario

- Precondición: Usuario autenticado es administrador (id_rol = 1). Usuario ID 5 tiene reservas.
- Acción: Ejecutar GET /api/v1/reservas/usuario/5.
- Resultado esperado:
- Código HTTP 200 OK
- Se devuelven las reservas del usuario ID 5

### ✅ Caso 3: Usuario sin reservas

- Precondición: Usuario autenticado con ID 6 no tiene reservas registradas.
- Acción: Ejecutar GET /api/v1/reservas/usuario/6.
- Resultado esperado:
- Código HTTP 200 OK
- data.reservas es un array vacío
- message = "El usuario no tiene reservas registradas"

### ❌ Caso 4: Usuario no encontrado

- Precondición: No existe usuario con ID 99.
- Acción: Ejecutar GET /api/v1/reservas/usuario/99.
- Resultado esperado:
- Código HTTP 404 Not Found
- error.error_code: USUARIO_NOT_FOUND

### ❌ Caso 5: Residente intenta consultar reservas de otro residente

- Precondición: Usuario autenticado con ID 5 (residente). Usuario ID 6 (residente) tiene reservas.
- Acción: Ejecutar GET /api/v1/reservas/usuario/6.
- Resultado esperado:
- Código HTTP 403 Forbidden
- error.error_code: ACCESO_DENEGADO

### ❌ Caso 6: Usuario no autenticado

- Precondición: El cliente no envía token de autenticación.
- Acción: Ejecutar GET /api/v1/reservas/usuario/5 sin header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- error.error_code: NO_AUTENTICADO

### ✅ Caso 7: Verificar ordenamiento por fecha descendente

- Precondición: Usuario tiene reservas en diferentes fechas.
- Acción: Ejecutar GET /api/v1/reservas/usuario/5.
- Resultado esperado:
- Las reservas se muestran ordenadas de la fecha más reciente a la más antigua

## ✅ Definición de Hecho

- Historia: [HU-012] Consulta de reservas

## 📦 Alcance Funcional

- [ ] El endpoint GET /api/v1/reservas/usuario/{id} está implementado.
- [ ] La validación de autenticación funciona correctamente.
- [ ] La validación de usuario existente funciona.
- [ ] La validación de permisos (propietario o administrador) funciona.
- [ ] Se retorna la información completa de cada reserva (incluyendo zona).
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