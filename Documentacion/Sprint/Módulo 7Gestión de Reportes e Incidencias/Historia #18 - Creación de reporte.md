## 📖 Historia de Usuario
Como residente del conjunto

Quiero que el sistema me permita reportar un daño o una queja describiendo el problema, seleccionando el tipo de reporte y adjuntando fotos como evidencia

Para que la administración conozca la situación de manera detallada y pueda tomar acciones para solucionarlo sin necesidad de que yo me desplace a la oficina

## 🔁 Flujo Esperado
Se recibe una petición POST en /api/v1/reportes con los datos del reporte en el cuerpo de la solicitud en formato JSON.

Se valida que el usuario esté autenticado.

Se valida que los campos requeridos (tipo, descripcion) estén presentes.

Se valida que el tipo sea válido (daño, queja, solicitud).

Se valida que la descripcion no esté vacía.

Se guarda el reporte en la tabla reportes con estado "pendiente".

Se guardan las rutas de las evidencias (fotos) si se enviaron.

Se retorna una respuesta JSON con código 201 Created y los datos del reporte creado.

## ✅ Criterios de Aceptación
## 1. 🔍 Estructura y lógica del servicio
Se expone un endpoint POST /api/v1/reportes para crear reportes de incidencias.

Se valida que el usuario esté autenticado.

Se valida que los campos tipo y descripcion sean obligatorios.

Se valida que tipo sea: "daño", "queja" o "solicitud".

Se asigna automáticamente el estado "pendiente" al nuevo reporte.

## 2. 📤 Estructura de la información
Respuesta de creación exitosa:
{
  "success": true,
  "statusCode": 201,
  "message": "Reporte creado exitosamente",
  "data": {
    "id_reporte": 1,
    "id_usuario": 5,
    "nombre_usuario": "Carlos Rodríguez",
    "tipo": "daño",
    "descripcion": "El bombillo del pasillo del tercer piso no funciona",
    "evidencias": [
      "/uploads/reportes/foto_1.jpg",
      "/uploads/reportes/foto_2.jpg"
    ],
    "estado": "pendiente",
    "fecha_reporte": "2026-04-29T10:30:00Z"
  }
}

## Respuesta de error por tipo inválido:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "TIPO_INVALIDO",
    "details": "El tipo debe ser: daño, queja o solicitud",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

## Respuesta de error por campo obligatorio faltante:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "CAMPO_REQUERIDO",
    "details": "El campo descripcion es obligatorio",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

## 🔧 Notas Técnicas
## Reglas de negocio
Cualquier usuario autenticado puede crear reportes.

El tipo de reporte debe ser uno de los siguientes: "daño", "queja" o "solicitud".

El estado inicial de todo reporte es "pendiente".

Las evidencias (fotos) son opcionales, pero si se envían, se almacenan en el servidor.

No se permiten reportes con descripción vacía.

## Base de datos (tabla reportes)
La tabla debe incluir las siguientes columnas:

id_reporte: SERIAL / AUTO_INCREMENT (PK)

id_usuario: INT, NOT NULL (FK usuarios.id_usuario)

tipo: ENUM('daño', 'queja', 'solicitud'), NOT NULL

descripcion: TEXT, NOT NULL

evidencias: TEXT (JSON o ruta separada por comas)

estado: ENUM('pendiente', 'en_proceso', 'resuelto'), DEFAULT 'pendiente'

responsable_id: INT, NULLABLE (FK usuarios.id_usuario)

fecha_reporte: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

fecha_resolucion: TIMESTAMP, NULLABLE

## Seguridad
Validar el token JWT antes de procesar la solicitud.

El id_usuario se obtiene del token, no del request body.

Validar el tipo y tamaño de los archivos de evidencia.

## Manejo de errores
Los códigos de error (NO_AUTENTICADO, TIPO_INVALIDO, CAMPO_REQUERIDO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Creación de reportes de incidencias
Método HTTP: POST

Ruta: /api/v1/reportes

Autenticación requerida: Sí (residente o administrador)

## 📤 Ejemplo de Request JSON
{
  "tipo": "daño",
  "descripcion": "El bombillo del pasillo del tercer piso no funciona",
  "evidencias": ["/uploads/reportes/foto_1.jpg", "/uploads/reportes/foto_2.jpg"]
}

## 📤 Ejemplo de Respuesta JSON Exitosa (201 Created)
{
  "success": true,
  "statusCode": 201,
  "message": "Reporte creado exitosamente",
  "data": {
    "id_reporte": 1,
    "id_usuario": 5,
    "nombre_usuario": "Carlos Rodríguez",
    "tipo": "daño",
    "descripcion": "El bombillo del pasillo del tercer piso no funciona",
    "evidencias": [
      "/uploads/reportes/foto_1.jpg",
      "/uploads/reportes/foto_2.jpg"
    ],
    "estado": "pendiente",
    "fecha_reporte": "2026-04-29T10:30:00Z"
  }
}

## 📤 Ejemplo de Respuesta JSON Error (400 Bad Request)
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "TIPO_INVALIDO",
    "details": "El tipo debe ser: daño, queja o solicitud",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
## ✅ Caso 1: Creación exitosa de reporte tipo "daño"
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/reportes con tipo = "daño" y descripcion válida.

Resultado esperado:

Código HTTP 201 Created

data.id_reporte contiene un número

data.estado = "pendiente"

Se guarda el reporte en la base de datos

## ✅ Caso 2: Creación exitosa de reporte tipo "queja"
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/reportes con tipo = "queja".

Resultado esperado:

Código HTTP 201 Created

data.tipo = "queja"

## ✅ Caso 3: Creación exitosa de reporte tipo "solicitud"
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/reportes con tipo = "solicitud".

Resultado esperado:

Código HTTP 201 Created

data.tipo = "solicitud"

## ✅ Caso 4: Creación de reporte con evidencias
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/reportes con evidencias (rutas de archivos).

Resultado esperado:

Las rutas de evidencias se guardan correctamente

data.evidencias contiene las rutas enviadas

## ❌ Caso 5: Tipo inválido
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/reportes con tipo = "reclamo".

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: TIPO_INVALIDO

## ❌ Caso 6: Descripción vacía
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/reportes con descripcion = "".

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: CAMPO_REQUERIDO

## ❌ Caso 7: Campo tipo obligatorio faltante
Precondición: Usuario autenticado.

Acción: Enviar POST /api/v1/reportes sin el campo tipo.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: CAMPO_REQUERIDO

## ❌ Caso 8: Usuario no autenticado
Precondición: El cliente no envía token de autenticación.

Acción: Enviar POST /api/v1/reportes sin header Authorization.

Resultado esperado:

Código HTTP 401 Unauthorized

error.error_code: NO_AUTENTICADO

## ✅ Definición de Hecho
Historia: [HU-018] Creación de reportes de incidencias
## 📦 Alcance Funcional
El endpoint POST /api/v1/reportes está implementado.

La validación de autenticación funciona correctamente.

La validación de campos obligatorios funciona.

La validación de tipo válido funciona.

El estado inicial "pendiente" se asigna automáticamente.

Las evidencias se almacenan correctamente.

## 🧪 Pruebas Completadas
Se ejecutaron pruebas unitarias para cada validación.

Se ejecutaron pruebas de integración para el flujo completo.

Se probaron todos los casos de error documentados.


## 📄 Documentación Técnica
Endpoint documentado en Swagger / OpenAPI.

Se describe: propósito del endpoint, campos de entrada y salida.

## 🔐 Manejo de Errores
Se devuelve código HTTP 400 para errores de validación.

Se devuelve código HTTP 401 para usuario no autenticado.

El campo error en el JSON incluye error_code, details y timestamp.

