## 📖 Historia de Usuario
Como residente del conjunto

Quiero que el sistema me muestre la lista de comunicados activos ordenados por fecha de publicación, con los más recientes primero, y que me permita abrir cada uno para ver su contenido completo y descargar los archivos adjuntos

Para estar al día de las noticias del conjunto sin necesidad de revisar carteleras físicas o grupos de WhatsApp

## 🔁 Flujo Esperado 
Se recibe una petición GET en /api/v1/comunicados/activos para consultar los comunicados activos.

Se valida que el usuario esté autenticado.

Se consulta la tabla comunicados filtrando por activo = true y fecha_expiracion > fecha_actual o fecha_expiracion IS NULL.

Se ordenan los resultados por fecha_publicacion descendente (más recientes primero).

Se retorna una respuesta JSON con la lista de comunicados activos.

## ✅ Criterios de Aceptación
## 1. 🔍 Estructura y lógica del servicio
Se expone un endpoint GET /api/v1/comunicados/activos para consultar comunicados activos.

Se valida que el usuario esté autenticado.

Se retornan solo los comunicados con activo = true.

Se excluyen comunicados con fecha_expiracion anterior a la fecha actual.

Se ordenan los resultados por fecha de publicación descendente.

## 2. 📤 Estructura de la información
Respuesta de consulta exitosa:
{
  "success": true,
  "statusCode": 200,
  "message": "Consulta exitosa",
  "data": {
    "comunicados": [
      {
        "id_comunicado": 2,
        "titulo": "Reunión de copropietarios",
        "contenido": "Se convoca a reunión el día 20 de mayo...",
        "autor": {
          "id_autor": 1,
          "nombre": "Administrador"
        },
        "archivos_adjuntos": [
          "/uploads/comunicados/orden_dia.pdf"
        ],
        "fecha_publicacion": "2026-04-28T15:30:00Z"
      },
      {
        "id_comunicado": 1,
        "titulo": "Corte de agua programado",
        "contenido": "El día 15 de mayo habrá corte de agua...",
        "autor": {
          "id_autor": 1,
          "nombre": "Administrador"
        },
        "archivos_adjuntos": [
          "/uploads/comunicados/aviso_agua.pdf"
        ],
        "fecha_publicacion": "2026-04-25T10:30:00Z"
      }
    ]
  }
}

## Respuesta cuando no hay comunicados activos:
{
  "success": true,
  "statusCode": 200,
  "message": "No hay comunicados activos en este momento",
  "data": {
    "comunicados": []
  }
}

## 🔧 Notas Técnicas
## Reglas de negocio
Cualquier usuario autenticado puede consultar los comunicados activos.

Un comunicado se considera inactivo si:

activo = false, o

fecha_expiracion no es nula y es menor a la fecha actual

Los comunicados deben mostrarse ordenados por fecha de publicación (más reciente primero).

## Base de datos (tabla comunicados)
Se debe consultar la tabla comunicados con los siguientes filtros:

activo = true

fecha_expiracion IS NULL OR fecha_expiracion > CURRENT_TIMESTAMP

Se debe hacer un JOIN con la tabla usuarios para obtener el nombre del autor.

## Seguridad
Validar el token JWT antes de procesar la solicitud.

No se requiere rol específico, cualquier usuario autenticado puede consultar.

## Manejo de errores
Los códigos de error (NO_AUTENTICADO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta de comunicados activos
Método HTTP: GET

Ruta: /api/v1/comunicados/activos

Autenticación requerida: Sí (residente o administrador)

## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
{
  "success": true,
  "statusCode": 200,
  "message": "Consulta exitosa",
  "data": {
    "comunicados": [
      {
        "id_comunicado": 2,
        "titulo": "Reunión de copropietarios",
        "contenido": "Se convoca a reunión el día 20 de mayo...",
        "autor": {
          "id_autor": 1,
          "nombre": "Administrador"
        },
        "archivos_adjuntos": [
          "/uploads/comunicados/orden_dia.pdf"
        ],
        "fecha_publicacion": "2026-04-28T15:30:00Z"
      },
      {
        "id_comunicado": 1,
        "titulo": "Corte de agua programado",
        "contenido": "El día 15 de mayo habrá corte de agua...",
        "autor": {
          "id_autor": 1,
          "nombre": "Administrador"
        },
        "archivos_adjuntos": [
          "/uploads/comunicados/aviso_agua.pdf"
        ],
        "fecha_publicacion": "2026-04-25T10:30:00Z"
      }
    ]
  }
}

## 📤 Ejemplo de Respuesta JSON (sin comunicados)
{
  "success": true,
  "statusCode": 200,
  "message": "No hay comunicados activos en este momento",
  "data": {
    "comunicados": []
  }
}

## 📤 Ejemplo de Respuesta JSON Error (401 Unauthorized)
{
  "success": false,
  "statusCode": 401,
  "message": "No autenticado",
  "error": {
    "error_code": "NO_AUTENTICADO",
    "details": "Se requiere un token de autenticación válido",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
## ✅ Caso 1: Consulta exitosa con comunicados activos
Precondición: Existen comunicados con activo = true y fecha de expiración futura o nula.

Acción: Ejecutar GET /api/v1/comunicados/activos.

Resultado esperado:

Código HTTP 200 OK

data.comunicados contiene los comunicados activos

Los resultados están ordenados por fecha descendente

## ✅ Caso 2: No hay comunicados activos
Precondición: No existen comunicados con activo = true o todos tienen fecha de expiración pasada.

Acción: Ejecutar GET /api/v1/comunicados/activos.

Resultado esperado:

Código HTTP 200 OK

data.comunicados es un array vacío

message = "No hay comunicados activos en este momento"

## ✅ Caso 3: Comunicado sin fecha de expiración
Precondición: Existe un comunicado con activo = true y fecha_expiracion = NULL.

Acción: Ejecutar GET /api/v1/comunicados/activos.

Resultado esperado:

El comunicado aparece en la lista (nunca expira)

## ❌ Caso 4: Comunicado expirado no aparece
Precondición: Existe un comunicado con activo = true pero fecha_expiracion es anterior a la fecha actual.

Acción: Ejecutar GET /api/v1/comunicados/activos.

Resultado esperado:

El comunicado expirado NO aparece en la lista

## ❌ Caso 5: Comunicado inactivo no aparece
Precondición: Existe un comunicado con activo = false.

Acción: Ejecutar GET /api/v1/comunicados/activos.

Resultado esperado:

El comunicado inactivo NO aparece en la lista

## ❌ Caso 6: Usuario no autenticado
Precondición: El cliente no envía token de autenticación.

Acción: Ejecutar GET /api/v1/comunicados/activos sin header Authorization.

Resultado esperado:

Código HTTP 401 Unauthorized

error.error_code: NO_AUTENTICADO

## ✅ Definición de Hecho
Historia: [HU-014] Consulta de comunicados
## 📦 Alcance Funcional
El endpoint GET /api/v1/comunicados/activos está implementado.

La validación de autenticación funciona correctamente.

Se retornan solo comunicados activos (no expirados).

Los resultados se ordenan correctamente por fecha descendente.

Se incluye la información del autor en cada comunicado.

## 🧪 Pruebas Completadas
Se ejecutaron pruebas unitarias para la consulta.

Se ejecutaron pruebas de integración para el flujo completo.

Se probaron todos los casos documentados.

## 📄 Documentación Técnica
Endpoint documentado en Swagger / OpenAPI.

Se describe: propósito del endpoint y salida.

## 🔐 Manejo de Errores
Se devuelve código HTTP 401 para usuario no autenticado.

El campo error en el JSON incluye error_code, details y timestamp.