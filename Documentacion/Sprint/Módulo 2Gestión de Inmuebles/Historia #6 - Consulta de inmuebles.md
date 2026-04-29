## 📖 Historia de Usuario
Como administrador del conjunto

Quiero que el sistema me permita consultar la lista de inmuebles aplicando filtros por torre, estado (ocupado/disponible) o nombre del propietario asignado

Para facilitar la búsqueda de información y tener un control detallado sobre la ocupación del conjunto

## 🔁 Flujo Esperado
Se recibe una petición GET en /api/v1/inmuebles con parámetros de consulta opcionales (torre, estado, nombre_propietario, page, limit).

Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).

Se construye la consulta a la base de datos aplicando los filtros enviados.

Se ejecuta la consulta con paginación.

Se retorna una respuesta JSON con código 200 OK y la lista de inmuebles que cumplen los filtros.

## ✅ Criterios de Aceptación

### 1. 🔍 Estructura y lógica del servicio
Se expone un endpoint GET /api/v1/inmuebles para consulta de inmuebles.

Se valida que el usuario autenticado sea administrador (id_rol = 1).

Se permite filtrar por torre (parámetro opcional).

Se permite filtrar por estado (parámetro opcional).

Se permite filtrar por nombre_propietario (parámetro opcional, búsqueda parcial).

Se implementa paginación con page y limit (parámetros opcionales).

Se incluye información del propietario en los resultados cuando existe.

### 2. 📆 Estructura de la información
Se responde con la siguiente estructura en JSON para consulta exitosa:
{
  "success": true,
  "statusCode": 200,
  "message": "Consulta exitosa",
  "data": {
    "inmuebles": [
      {
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
      },
      {
        "id_inmueble": 2,
        "numero": "102",
        "torre": "A",
        "area_m2": 75.5,
        "estado": "disponible",
        "propietario": null
      }
    ],
    "paginacion": {
      "total": 10,
      "page": 1,
      "limit": 10,
      "total_paginas": 1
    }
  }
}
Respuesta cuando no hay inmuebles:
{
  "success": true,
  "statusCode": 200,
  "message": "No se encontraron inmuebles",
  "data": {
    "inmuebles": [],
    "paginacion": {
      "total": 0,
      "page": 1,
      "limit": 10,
      "total_paginas": 0
    }
  }
}
Respuesta de error por filtro inválido:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "FILTRO_INVALIDO",
    "details": "El estado debe ser: disponible, ocupado o mantenimiento",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🔧 Notas Técnicas
## Reglas de negocio
Solo los administradores pueden registrar zonas comunes.

El nombre de la zona debe ser único en el conjunto.

La capacidad máxima debe ser un número positivo.

Una zona en estado "mantenimiento" no puede ser reservada.

## Base de datos (tabla zonas_comunes)
La tabla debe incluir las siguientes columnas:

id_zona: SERIAL / AUTO_INCREMENT (PK)

nombre: VARCHAR(100), UNIQUE, NOT NULL

capacidad_maxima: INT, NOT NULL

descripcion: TEXT

reglas_uso: TEXT

estado: ENUM('disponible', 'mantenimiento'), DEFAULT 'disponible'

horario_inicio: TIME

horario_fin: TIME

fecha_registro: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

## Seguridad
Validar el token JWT antes de procesar la solicitud.

Verificar que el usuario tenga rol de administrador.

## Manejo de errores
Los códigos de error deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta del Último Cierre
Método HTTP: GET

Ruta: /api/v1/inmuebles

Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Respuesta JSON
URL: GET /api/v1/inmuebles?torre=A&estado=ocupado&page=1&limit=10

📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
{
  "success": true,
  "statusCode": 200,
  "message": "Consulta exitosa",
  "data": {
    "inmuebles": [
      {
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
      },
      {
        "id_inmueble": 3,
        "numero": "103",
        "torre": "A",
        "area_m2": 85.0,
        "estado": "ocupado",
        "propietario": {
          "id_propietario": 7,
          "nombre_completo": "Ana Martínez",
          "email": "ana@example.com",
          "telefono": "3001234567"
        }
      }
    ],
    "paginacion": {
      "total": 2,
      "page": 1,
      "limit": 10,
      "total_paginas": 1
    }
  }
}
📤 Ejemplo de Respuesta JSON Error (403 Forbidden)
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "ACCESO_DENEGADO",
    "details": "Se requiere rol de administrador para consultar todos los inmuebles",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Consulta exitosa sin filtros
Precondición: Usuario autenticado es administrador. Existen inmuebles registrados.

Acción: Ejecutar GET /api/v1/inmuebles sin parámetros.

Resultado esperado:

Código HTTP 200 OK

success: true

data.inmuebles contiene todos los inmuebles (paginados)

Los resultados están ordenados por torre y numero

### ✅ Caso 2: Consulta con filtro por torre
Precondición: Usuario autenticado es administrador. Existen inmuebles en torre A y torre B.

Acción: Ejecutar GET /api/v1/inmuebles?torre=A.

Resultado esperado:

Código HTTP 200 OK

Solo se devuelven inmuebles de la torre A

Los inmuebles de torre B no aparecen en la respuesta

### ✅ Caso 3: Consulta con filtro por estado
Precondición: Usuario autenticado es administrador. Existen inmuebles "disponible" y "ocupado".

Acción: Ejecutar GET /api/v1/inmuebles?estado=disponible.

Resultado esperado:

Código HTTP 200 OK

Solo se devuelven inmuebles con estado "disponible"

### ✅ Caso 4: Consulta con filtro por nombre de propietario
Precondición: Usuario autenticado es administrador. Existe inmueble con propietario "Carlos Rodríguez".

Acción: Ejecutar GET /api/v1/inmuebles?nombre_propietario=Carlos.

Resultado esperado:

Código HTTP 200 OK

Se devuelven inmuebles cuyo propietario contiene "Carlos" en el nombre

### ✅ Caso 5: Consulta con paginación
Precondición: Usuario autenticado es administrador. Existen 25 inmuebles registrados.

Acción: Ejecutar GET /api/v1/inmuebles?page=2&limit=10.

Resultado esperado:

Código HTTP 200 OK

data.inmuebles contiene 10 inmuebles (los de la página 2)

data.paginacion.total = 25

data.paginacion.total_paginas = 3

### ✅ Caso 6: Consulta con múltiples filtros combinados
Precondición: Usuario autenticado es administrador.

Acción: Ejecutar GET /api/v1/inmuebles?torre=A&estado=ocupado&nombre_propietario=Carlos.

Resultado esperado:

Código HTTP 200 OK

Solo se devuelven inmuebles que cumplen TODOS los filtros

### ✅ Caso 7: No se encuentran inmuebles
Precondición: Usuario autenticado es administrador. No existen inmuebles con estado "mantenimiento".

Acción: Ejecutar GET /api/v1/inmuebles?estado=mantenimiento.

Resultado esperado:

Código HTTP 200 OK

data.inmuebles es un array vacío

data.paginacion.total = 0

message = "No se encontraron inmuebles"

### ❌ Caso 8: Filtro estado inválido
Precondición: Usuario autenticado es administrador.

Acción: Ejecutar GET /api/v1/inmuebles?estado=invalido.

Resultado esperado:

Código HTTP 400 Bad Request

success: false

error.error_code: FILTRO_INVALIDO

### ❌ Caso 9: Usuario no autenticado
Precondición: El cliente no envía token de autenticación.

Acción: Ejecutar GET /api/v1/inmuebles sin header Authorization.

Resultado esperado:

Código HTTP 401 Unauthorized

success: false

error.error_code: NO_AUTENTICADO

### ❌ Caso 10: Usuario autenticado no es administrador
Precondición: El token pertenece a un usuario con id_rol = 2 (residente).

Acción: Ejecutar GET /api/v1/inmuebles con token de residente.

Resultado esperado:

Código HTTP 403 Forbidden

success: false

error.error_code: ACCESO_DENEGADO

## ✅ Definición de Hecho
Historia: [HU-006] Consulta de inmuebles

## 📦 Alcance Funcional
El endpoint GET /api/v1/inmuebles está implementado.

La validación de autenticación funciona correctamente.

La validación de permisos (solo administradores) funciona.

Los filtros por torre, estado y nombre_propietario funcionan.

La paginación funciona correctamente.

La información del propietario se incluye cuando existe.

Los resultados están ordenados correctamente.

Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas
Se ejecutaron pruebas unitarias para la construcción de consultas.

Se ejecutaron pruebas de integración para el flujo completo.

Se probaron todos los casos de error documentados.

Se probaron todas las combinaciones de filtros.

Se verificó el funcionamiento de la paginación.

## 📄 Documentación Técnica
Endpoint documentado en Swagger / OpenAPI.

Se describe: propósito del endpoint, parámetros de consulta y salida.

Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores
Se devuelve código HTTP 400 para parámetros inválidos.

Se devuelve código HTTP 401 para usuario no autenticado.

Se devuelve código HTTP 403 para permisos insuficientes.

El campo error en el JSON incluye error_code, details y timestamp.