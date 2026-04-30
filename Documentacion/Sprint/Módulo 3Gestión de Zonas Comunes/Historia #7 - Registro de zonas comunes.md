## 📖 Historia de Usuario

Como administrador del conjunto

Quiero que el sistema me permita registrar las zonas comunes del conjunto como salón social, canchas deportivas o piscina, ingresando su nombre, capacidad máxima de personas y horarios permitidos de uso

Para que los residentes puedan conocer los espacios disponibles y las condiciones para reservarlos

## 🔁 Flujo Esperado 

- Se recibe una petición POST en /api/v1/zonas con los datos de la zona común en el cuerpo de la solicitud en formato JSON.
- Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).
- Se valida que todos los campos requeridos (nombre, capacidad_maxima) estén presentes.
- Se valida que capacidad_maxima sea un número entero mayor a 0.
- Se valida que el nombre de la zona no esté duplicado en la base de datos.
- Se guarda la nueva zona común en la tabla zonas_comunes con estado "disponible" y fecha_registro actual.
- Se retorna una respuesta JSON con código 201 Created y los datos de la zona creada.
- El backend retorna una respuesta JSON con código 201 Created y los datos de la zona creada.

## ✅ Criterios de Aceptación

## 1. 🔍 Estructura y lógica del servicio

- [ ] Se expone un endpoint POST /api/v1/zonas para registro de zonas comunes.
- [ ] Se valida que el usuario autenticado sea administrador (id_rol = 1).
- [ ] Se valida que los campos nombre y capacidad_maxima sean obligatorios.
- [ ] Se valida que capacidad_maxima sea un número entero mayor a 0.
- [ ] Se valida que el nombre de la zona sea único.
- [ ] Se asigna automáticamente el estado "disponible" a la nueva zona.

## 2. 📤 Estructura de la información

- [ ] Se responde con la siguiente estructura en JSON para registro exitoso:
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Zona común registrada exitosamente",
  "data": {
    "id_zona": 1,
    "nombre": "Salón Social",
    "capacidad_maxima": 50,
    "descripcion": "Espacio para eventos y reuniones",
    "estado": "disponible",
    "horario_inicio": "08:00",
    "horario_fin": "22:00",
    "fecha_registro": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por zona duplicada:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "ZONA_DUPLICADA",
    "details": "Ya existe una zona común con el nombre 'Salón Social'",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por capacidad inválida:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "CAPACIDAD_INVALIDA",
    "details": "La capacidad máxima debe ser un número entero mayor a 0",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
- [ ] Respuesta de error por campo obligatorio faltante:
```json
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "CAMPO_REQUERIDO",
    "details": "El campo nombre es obligatorio",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
## 🔧 Notas Técnicas

## Reglas de negocio

- Solo los administradores pueden registrar zonas comunes.
- El nombre de la zona debe ser único en el conjunto.
- La capacidad máxima debe ser un número entero positivo.
- Por defecto, el estado inicial de una zona es "disponible".
- Los horarios de uso son opcionales al registrar, pero pueden definirse después.

## Base de datos (tabla zonas_comunes)

- La tabla debe incluir las siguientes columnas:

- id_zona: SERIAL / AUTO_INCREMENT (PK)
- nombre: VARCHAR(100), UNIQUE, NOT NULL
- capacidad_maxima: INT, NOT NULL
- descripcion: TEXT
- estado: ENUM('disponible', 'mantenimiento'), DEFAULT 'disponible'
- horario_inicio: TIME
- horario_fin: TIME
- fecha_registro: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP

## Seguridad

- Validar el token JWT antes de procesar la solicitud.
- Verificar que el usuario tenga rol de administrador (id_rol = 1).

## Manejo de errores

- Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, ZONA_DUPLICADA, CAPACIDAD_INVALIDA, CAMPO_REQUERIDO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Registro de zonas comunes

- Método HTTP: POST
- Ruta: /api/v1/zonas
- Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Request JSON
```json
{
  "nombre": "Salón Social",
  "capacidad_maxima": 50,
  "descripcion": "Espacio para eventos y reuniones familiares",
  "horario_inicio": "08:00",
  "horario_fin": "22:00"
}
```
## 📤 Ejemplo de Respuesta JSON Exitosa (201 Created)
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Zona común registrada exitosamente",
  "data": {
    "id_zona": 1,
    "nombre": "Salón Social",
    "capacidad_maxima": 50,
    "descripcion": "Espacio para eventos y reuniones familiares",
    "estado": "disponible",
    "horario_inicio": "08:00",
    "horario_fin": "22:00",
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
    "error_code": "ZONA_DUPLICADA",
    "details": "Ya existe una zona común con el nombre 'Salón Social'",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}
```
## 🧪 Requisitos de Pruebas

## 🔍 Casos de Prueba Funcional

### ✅ Caso 1: Registro exitoso de zona común

- Precondición: Usuario autenticado es administrador. No existe zona "Salón Social".
- Acción: Ejecutar POST /api/v1/zonas con los datos de ejemplo.
- Resultado esperado:
- Código HTTP 201 Created
- success: true
- data.id_zona contiene un número
- data.estado = "disponible"

### ❌ Caso 2: Nombre de zona duplicado

- Precondición: Ya existe una zona "Salón Social" en la base de datos.
- Acción: Enviar POST /api/v1/zonas con nombre "Salón Social".
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: ZONA_DUPLICADA

### ❌ Caso 3: Capacidad inválida (cero o negativa)

- Precondición: Usuario autenticado es administrador.
- Acción: Enviar POST /api/v1/zonas con capacidad_maxima = 0.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: CAPACIDAD_INVALIDA

### ❌ Caso 4: Capacidad no es un número entero

- Precondición: Usuario autenticado es administrador.
- Acción: Enviar POST /api/v1/zonas con capacidad_maxima = 50.5.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: CAPACIDAD_INVALIDA

### ❌ Caso 5: Campo obligatorio faltante

- Precondición: Usuario autenticado es administrador.
- Acción: Enviar POST /api/v1/zonas sin el campo nombre.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: CAMPO_REQUERIDO

### ❌ Caso 6: Usuario no autenticado

- Precondición: El cliente no envía token de autenticación.
- Acción: Enviar POST /api/v1/zonas sin header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: NO_AUTENTICADO

### ❌ Caso 7: Usuario autenticado no es administrador

- Precondición: El token pertenece a un usuario con id_rol = 2 (residente).
- Acción: Enviar POST /api/v1/zonas con token de residente.
- Resultado esperado:
- Código HTTP 403 Forbidden
- success: false
- error.error_code: ACCESO_DENEGADO

## ✅ Definición de Hecho

- Historia: [HU-007] Registro de zonas comunes

## 📦 Alcance Funcional

- [ ] El endpoint POST /api/v1/zonas está implementado.
- [ ] Las validaciones de campos obligatorios funcionan.
- [ ] La validación de unicidad del nombre funciona.
- [ ] La validación de capacidad positiva funciona.
- [ ] La validación de autenticación y permisos funciona (solo administradores).
- [ ] El estado inicial "disponible" se asigna automáticamente.
- [ ] Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas

- [ ] Se ejecutaron pruebas unitarias para cada validación.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.

## 📄 Documentación Técnica

- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, campos de entrada y salida.
- [ ] Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores

- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para permisos insuficientes.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.