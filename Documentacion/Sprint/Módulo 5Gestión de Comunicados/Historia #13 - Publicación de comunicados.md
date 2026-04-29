## 📖 Historia de Usuario
Como administrador del conjunto

Quiero que el sistema me permita publicar comunicados ingresando un título, una descripción detallada y archivos adjuntos como PDF o imágenes, y que me permita programar una fecha de expiración si el aviso es temporal

Para informar a todos los residentes sobre avisos importantes como reuniones, cortes de servicios o cambios en las reglas del conjunto

## 🔁 Flujo Esperado 
Se recibe una petición POST en /api/v1/comunicados con los datos del comunicado en el cuerpo de la solicitud en formato JSON.

Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).

Se valida que los campos requeridos (titulo, contenido) estén presentes.

Se valida que la fecha de expiración, si se envía, no sea anterior a la fecha actual.

Se guarda el comunicado en la tabla comunicados con estado "activo".

Se guarda la ruta de los archivos adjuntos si se enviaron.

Se retorna una respuesta JSON con código 201 Created y los datos del comunicado creado.

## ✅ Criterios de Aceptación
## 1. 🔍 Estructura y lógica del servicio
Se expone un endpoint POST /api/v1/comunicados para publicación de comunicados.

Se valida que el usuario autenticado sea administrador (id_rol = 1).

Se valida que los campos titulo y contenido sean obligatorios.

Se valida que la fecha de expiración, si existe, no sea anterior a la actual.

Se asigna automáticamente el estado "activo" y la fecha de publicación actual.

## 2. 📤 Estructura de la información
Respuesta de publicación exitosa:
{
  "success": true,
  "statusCode": 201,
  "message": "Comunicado publicado exitosamente",
  "data": {
    "id_comunicado": 1,
    "titulo": "Corte de agua programado",
    "contenido": "El día 15 de mayo habrá corte de agua de 8:00 a 12:00...",
    "id_autor": 1,
    "autor_nombre": "Administrador",
    "archivos_adjuntos": [
      "/uploads/comunicados/aviso_agua.pdf"
    ],
    "fecha_publicacion": "2026-04-29T10:30:00Z",
    "fecha_expiracion": "2026-05-16T00:00:00Z",
    "activo": true
  }
}

Respuesta de error por campos obligatorios faltantes:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "CAMPO_REQUERIDO",
    "details": "El campo titulo es obligatorio",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

Respuesta de error por fecha de expiración inválida:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "FECHA_EXPIRACION_INVALIDA",
    "details": "La fecha de expiración no puede ser anterior a la fecha actual",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

## 🔧 Notas Técnicas
## Reglas de negocio
Solo los administradores pueden publicar comunicados.

La fecha de publicación se asigna automáticamente al momento de crear el comunicado.

El estado inicial de todo comunicado es "activo".

Los archivos adjuntos se almacenan en el servidor y se guarda la ruta en la base de datos.

La fecha de expiración es opcional; si no se envía, el comunicado no expira.

## Base de datos (tabla comunicados)
La tabla debe incluir las siguientes columnas:

id_comunicado: SERIAL / AUTO_INCREMENT (PK)

titulo: VARCHAR(200), NOT NULL

contenido: TEXT, NOT NULL

id_autor: INT, NOT NULL (FK usuarios.id_usuario)

archivos_adjuntos: TEXT (JSON o ruta separada por comas)

fecha_publicacion: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

fecha_expiracion: TIMESTAMP, NULLABLE

activo: BOOLEAN, DEFAULT TRUE

## Seguridad
Validar el token JWT antes de procesar la solicitud.

Verificar que el usuario tenga rol de administrador (id_rol = 1).

Validar el tipo y tamaño de los archivos adjuntos (ej: solo PDF, imágenes, máx 5MB).

## Manejo de errores
Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, CAMPO_REQUERIDO, FECHA_EXPIRACION_INVALIDA) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Publicación de comunicados
Método HTTP: POST
Ruta: /api/v1/comunicados
Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Request JSON
{
  "titulo": "Corte de agua programado",
  "contenido": "El día 15 de mayo habrá corte de agua de 8:00 a 12:00 por mantenimiento.",
  "archivos_adjuntos": ["/uploads/comunicados/aviso_agua.pdf"],
  "fecha_expiracion": "2026-05-16T00:00:00Z"
}

## 📤 Ejemplo de Respuesta JSON Exitosa (201 Created)
{
  "success": true,
  "statusCode": 201,
  "message": "Comunicado publicado exitosamente",
  "data": {
    "id_comunicado": 1,
    "titulo": "Corte de agua programado",
    "contenido": "El día 15 de mayo habrá corte de agua de 8:00 a 12:00 por mantenimiento.",
    "id_autor": 1,
    "autor_nombre": "Administrador",
    "archivos_adjuntos": [
      "/uploads/comunicados/aviso_agua.pdf"
    ],
    "fecha_publicacion": "2026-04-29T10:30:00Z",
    "fecha_expiracion": "2026-05-16T00:00:00Z",
    "activo": true
  }
}

## 📤 Ejemplo de Respuesta JSON Error (403 Forbidden)
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "ACCESO_DENEGADO",
    "details": "Se requiere rol de administrador para publicar comunicados",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
## ✅ Caso 1: Publicación exitosa de comunicado
Precondición: Usuario autenticado es administrador.

Acción: Enviar POST /api/v1/comunicados con datos válidos.

Resultado esperado:

Código HTTP 201 Created

data.id_comunicado contiene un número

data.fecha_publicacion se asigna automáticamente

data.activo = true

## ❌ Caso 2: Título obligatorio faltante
Precondición: Usuario autenticado es administrador.

Acción: Enviar POST /api/v1/comunicados sin el campo titulo.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: CAMPO_REQUERIDO

## ❌ Caso 3: Contenido obligatorio faltante
Precondición: Usuario autenticado es administrador.

Acción: Enviar POST /api/v1/comunicados sin el campo contenido.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: CAMPO_REQUERIDO

## ❌ Caso 4: Fecha de expiración anterior a la actual
Precondición: Usuario autenticado es administrador. Hoy es 2026-04-29.

Acción: Enviar POST /api/v1/comunicados con fecha_expiracion = "2026-04-28T00:00:00Z".

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: FECHA_EXPIRACION_INVALIDA

## ❌ Caso 5: Usuario no autenticado
Precondición: El cliente no envía token de autenticación.

Acción: Enviar POST /api/v1/comunicados sin header Authorization.

Resultado esperado:

Código HTTP 401 Unauthorized

error.error_code: NO_AUTENTICADO

## ❌ Caso 6: Usuario autenticado no es administrador
Precondición: Usuario autenticado es residente (id_rol = 2).

Acción: Enviar POST /api/v1/comunicados con token de residente.

Resultado esperado:

Código HTTP 403 Forbidden

error.error_code: ACCESO_DENEGADO

## ✅ Caso 7: Comunicado sin fecha de expiración
Precondición: Usuario autenticado es administrador.

Acción: Enviar POST /api/v1/comunicados sin el campo fecha_expiracion.

Resultado esperado:

Código HTTP 201 Created

data.fecha_expiracion es null en la base de datos

## ✅ Definición de Hecho
Historia: [HU-013] Publicación de comunicados
## 📦 Alcance Funcional
El endpoint POST /api/v1/comunicados está implementado.

La validación de autenticación funciona correctamente.

La validación de permisos (solo administradores) funciona.

La validación de campos obligatorios funciona.

La validación de fecha de expiración funciona.

La fecha de publicación se asigna automáticamente.

El estado "activo" se asigna automáticamente.

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

Se devuelve código HTTP 403 para permisos insuficientes.

El campo error en el JSON incluye error_code, details y timestamp.

