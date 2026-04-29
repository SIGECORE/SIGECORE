## 📖 Historia de Usuario
Como administrador del conjunto

Quiero que el sistema me genere un reporte de cartera con la lista de residentes que tienen pagos pendientes, mostrando el valor adeudado, los meses de mora y los datos de contacto de cada uno

Para identificar a los morosos, enviar recordatorios de pago y tomar decisiones administrativas

## 🔁 Flujo Esperado
Se recibe una petición GET en /api/v1/pagos/reporte-cartera con parámetros de consulta opcionales.

Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).

Se consulta la tabla pagos para obtener todos los pagos registrados.

Se identifican los inmuebles que tienen pagos pendientes (meses sin pagar).

Se calcula el valor adeudado por cada inmueble (valor cuota × meses mora).

Se agrupan los resultados por inmueble y propietario.

Se retorna una respuesta JSON con el reporte de cartera.

## ✅ Criterios de Aceptación
### 1. 🔍 Estructura y lógica del servicio
Se expone un endpoint GET /api/v1/pagos/reporte-cartera para generar reporte de cartera.

Se valida que el usuario autenticado sea administrador (id_rol = 1).

Se permite filtrar por torre (parámetro opcional).

Se permite filtrar por meses_mora mínimo (parámetro opcional).

Se calcula el valor adeudado basado en la cuota de administración mensual.

### 2. 📤 Estructura de la información
Respuesta de reporte exitoso:
{
  "success": true,
  "statusCode": 200,
  "message": "Reporte generado exitosamente",
  "data": {
    "fecha_generacion": "2026-04-29T10:30:00Z",
    "total_morosos": 2,
    "total_adeudado": 600000.00,
    "cartera": [
      {
        "inmueble": {
          "id_inmueble": 1,
          "numero": "101",
          "torre": "A",
          "area_m2": 75.5
        },
        "propietario": {
          "id_propietario": 5,
          "nombre_completo": "Carlos Rodríguez",
          "email": "carlos@example.com",
          "telefono": "3009876543"
        },
        "meses_mora": 4,
        "valor_cuota": 150000.00,
        "total_adeudado": 600000.00,
        "ultimo_pago": "2025-12-15"
      },
      {
        "inmueble": {
          "id_inmueble": 2,
          "numero": "102",
          "torre": "A",
          "area_m2": 75.5
        },
        "propietario": {
          "id_propietario": 6,
          "nombre_completo": "Ana Martínez",
          "email": "ana@example.com",
          "telefono": "3001234567"
        },
        "meses_mora": 2,
        "valor_cuota": 150000.00,
        "total_adeudado": 300000.00,
        "ultimo_pago": "2026-02-10"
      }
    ]
  }
}
## Respuesta cuando no hay morosos:
{
  "success": true,
  "statusCode": 200,
  "message": "No hay residentes con pagos pendientes",
  "data": {
    "fecha_generacion": "2026-04-29T10:30:00Z",
    "total_morosos": 0,
    "total_adeudado": 0,
    "cartera": []
  }
}
## Respuesta de error por filtro inválido:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "FILTRO_INVALIDO",
    "details": "El parámetro meses_mora debe ser un número entero positivo",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
## Notas Técnicas 
## Reglas de negocio
Solo los administradores pueden generar el reporte de cartera.

La cuota de administración es un valor configurable por el sistema (ej: $150.000 mensuales).

Los meses de mora se calculan desde el último pago registrado hasta la fecha actual.

Si un inmueble nunca ha pagado, la mora es desde la fecha de registro.

El reporte puede filtrarse por torre o por cantidad de meses en mora.

## Base de datos (tablas pagos, inmuebles y usuarios)
Se debe consultar la tabla pagos para obtener el último pago de cada inmueble.

Se debe hacer un JOIN con inmuebles y usuarios para obtener los datos completos.

Los inmuebles sin pagos se consideran en mora desde su fecha de registro.

## Seguridad
Validar el token JWT antes de procesar la solicitud.

Verificar que el usuario tenga rol de administrador (id_rol = 1).

## Manejo de errores
Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, FILTRO_INVALIDO) deben ser constantes definidas en un archivo de errores del sistema.
## 🚀 Endpoint – Reporte de cartera
Método HTTP: GET

Ruta: /api/v1/pagos/reporte-cartera

Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Request
URL: GET /api/v1/pagos/reporte-cartera?torre=A&meses_mora=3

## 📤 Ejemplo de Respuesta JSON Exitosa (200 OK)
{
  "success": true,
  "statusCode": 200,
  "message": "Reporte generado exitosamente",
  "data": {
    "fecha_generacion": "2026-04-29T10:30:00Z",
    "total_morosos": 2,
    "total_adeudado": 600000.00,
    "cartera": [
      {
        "inmueble": {
          "id_inmueble": 1,
          "numero": "101",
          "torre": "A",
          "area_m2": 75.5
        },
        "propietario": {
          "id_propietario": 5,
          "nombre_completo": "Carlos Rodríguez",
          "email": "carlos@example.com",
          "telefono": "3009876543"
        },
        "meses_mora": 4,
        "valor_cuota": 150000.00,
        "total_adeudado": 600000.00,
        "ultimo_pago": "2025-12-15"
      }
    ]
  }
}
## 📤 Ejemplo de Respuesta JSON Error (403 Forbidden)
{
  "success": false,
  "statusCode": 403,
  "message": "Acceso denegado",
  "error": {
    "error_code": "ACCESO_DENEGADO",
    "details": "Se requiere rol de administrador para generar el reporte de cartera",
    "timestamp": "2026-04-29T10:30:00Z"
  }
}
## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
### ✅ Caso 1: Generar reporte sin filtros
Precondición: Usuario autenticado es administrador. Existen inmuebles con pagos pendientes.

Acción: Ejecutar GET /api/v1/pagos/reporte-cartera.

Resultado esperado:

Código HTTP 200 OK

data.total_morosos es el número de morosos

data.total_adeudado es la suma de todas las deudas

data.cartera contiene la lista de morosos

### ✅ Caso 2: Generar reporte con filtro por torre
Precondición: Usuario autenticado es administrador. Existen morosos en torre A y torre B.

Acción: Ejecutar GET /api/v1/pagos/reporte-cartera?torre=A.

Resultado esperado:

Solo aparecen morosos de la torre A

Los morosos de torre B no aparecen en el reporte

### ✅ Caso 3: Generar reporte con filtro por meses de mora
Precondición: Usuario autenticado es administrador. Existe un moroso con 4 meses y otro con 2 meses.

Acción: Ejecutar GET /api/v1/pagos/reporte-cartera?meses_mora=3.

Resultado esperado:

Solo aparece el moroso con 4 meses de mora

El moroso con 2 meses NO aparece

### ✅ Caso 4: No hay morosos
Precondición: Usuario autenticado es administrador. Todos los residentes están al día con sus pagos.

Acción: Ejecutar GET /api/v1/pagos/reporte-cartera.

Resultado esperado:

Código HTTP 200 OK

data.total_morosos = 0

data.total_adeudado = 0

data.cartera es un array vacío

message = "No hay residentes con pagos pendientes"

### ❌ Caso 5: Filtro meses_mora inválido
Precondición: Usuario autenticado es administrador.

Acción: Ejecutar GET /api/v1/pagos/reporte-cartera?meses_mora=0.

Resultado esperado:

Código HTTP 400 Bad Request

error.error_code: FILTRO_INVALIDO

### ❌ Caso 6: Usuario no autenticado
Precondición: El cliente no envía token de autenticación.

Acción: Ejecutar GET /api/v1/pagos/reporte-cartera sin header Authorization.

Resultado esperado:

Código HTTP 401 Unauthorized

error.error_code: NO_AUTENTICADO

### ❌ Caso 7: Usuario autenticado no es administrador
Precondición: Usuario autenticado es residente (id_rol = 2).

Acción: Ejecutar GET /api/v1/pagos/reporte-cartera con token de residente.

Resultado esperado:

Código HTTP 403 Forbidden

error.error_code: ACCESO_DENEGADO

### ✅ Caso 8: Verificar cálculo de total_adeudado
Precondición: Moroso con 4 meses de mora y cuota de $150.000.

Acción: Generar reporte.

Resultado esperado:

total_adeudado = 600000 para ese moroso

El cálculo es correcto (meses_mora × valor_cuota)

## ✅ Definición de Hecho
Historia: [HU-017] Reporte de cartera
## 📦 Alcance Funcional
El endpoint GET /api/v1/pagos/reporte-cartera está implementado.

La validación de autenticación funciona correctamente.

La validación de permisos (solo administradores) funciona.

Los filtros por torre y meses_mora funcionan.

El cálculo de meses de mora es correcto.

El cálculo del valor adeudado es correcto.

Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas
Se ejecutaron pruebas unitarias para el cálculo de mora.

Se ejecutaron pruebas de integración para el flujo completo.

Se probaron todos los casos de error documentados.

Se probaron todas las combinaciones de filtros.

## 📄 Documentación Técnica
Endpoint documentado en Swagger / OpenAPI.

Se describe: propósito del endpoint, parámetros de consulta y salida.

## 🔐 Manejo de Errores
Se devuelve código HTTP 400 para parámetros inválidos.

Se devuelve código HTTP 401 para usuario no autenticado.

Se devuelve código HTTP 403 para permisos insuficientes.

El campo error en el JSON incluye error_code, details y timestamp.

