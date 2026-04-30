## 📖 Historia de Usuario

Como administrador del conjunto

Quiero que el sistema me permita registrar los apartamentos o casas del conjunto ingresando su número identificador, la torre o bloque al que pertenecen y el área en metros cuadrados

Para llevar un inventario actualizado de todos los inmuebles que pertenecen al conjunto residencial

## 🔁 Flujo Esperado
- Se recibe una petición POST en /api/v1/inmuebles con los datos del inmueble en el cuerpo de la solicitud en formato JSON.
- Se valida que el usuario autenticado tenga rol de administrador (id_rol = 1).
- Se valida que todos los campos requeridos (numero, torre, area_m2) estén presentes.
- Se valida que area_m2 sea un número mayor a 0.
- Se valida que no exista otro inmueble con el mismo numero en la misma torre.
- Se guarda el nuevo inmueble en la tabla inmuebles con estado "disponible" y fecha_registro actual.
- Se retorna una respuesta JSON con código 201 Created y los datos del inmueble creado.

## ✅ Criterios de Aceptación
### 1. 🔍 Estructura y lógica del servicio
- [ ] Se expone un endpoint POST /api/v1/inmuebles para registro de inmuebles.
- [ ] Se valida que el usuario autenticado sea administrador (id_rol = 1).
- [ ] Se valida que los campos numero, torre y area_m2 sean obligatorios.
- [ ] Se valida que area_m2 sea un número mayor a 0.
- [ ] Se valida que no exista otro inmueble con el mismo numero en la misma torre.
- [ ] Se asigna automáticamente el estado "disponible" al nuevo inmueble.

### 2. 📆 Estructura de la información
- [ ] Se responde con la siguiente estructura en JSON para registro exitoso:
```json
{
  "success": true,
  "statusCode": 201,
  "message": "Inmueble registrado exitosamente",
  "data": {
    "id_inmueble": 1,
    "numero": "101",
    "torre": "A",
    "area_m2": 75.5,
    "estado": "disponible",
    "fecha_registro": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por inmueble duplicado:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "INMUEBLE_DUPLICADO",
    "details": "Ya existe un inmueble con el número 101 en la torre A",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por área inválida:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "AREA_INVALIDA",
    "details": "El área debe ser un número mayor a 0",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

- [ ] Respuesta de error por campo obligatorio faltante:
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "CAMPO_REQUERIDO",
    "details": "El campo numero es obligatorio",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🔧 Notas Técnicas
## Reglas de negocio
- Solo los administradores pueden registrar nuevos inmuebles.
- La combinación numero + torre debe ser única en el conjunto residencial.
- El estado inicial del inmueble siempre es "disponible".
- El área se almacena en metros cuadrados con 2 decimales.

## Base de datos (tabla inmuebles)
- La tabla debe incluir las siguientes columnas:

- id_inmueble: SERIAL / AUTO_INCREMENT (PK)
- numero: VARCHAR(10), NOT NULL
- torre: VARCHAR(10), NOT NULL
- area_m2: DECIMAL(10,2), NOT NULL
- estado: ENUM('disponible', 'ocupado', 'mantenimiento'), DEFAULT 'disponible'
- fecha_registro: TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
- id_propietario: INT, NULLABLE (FK referenciando usuarios.id_usuario)
- Restricción única: UNIQUE(numero, torre)

## Seguridad
- Validar el token JWT antes de procesar la solicitud.
- Verificar que id_rol del token sea 1 (administrador).
- Sanitizar los campos de texto para evitar inyección SQL.

## Manejo de errores
- Los códigos de error (NO_AUTENTICADO, ACCESO_DENEGADO, INMUEBLE_DUPLICADO, AREA_INVALIDA, CAMPO_REQUERIDO) deben ser constantes definidas en un archivo de errores del sistema.

## 🚀 Endpoint – Consulta del Último Cierre
- Método HTTP: POST
- Ruta: /api/v1/inmuebles
- Autenticación requerida: Sí (solo administradores)

## 📤 Ejemplo de Request JSON
{
  "numero": "101",
  "torre": "A",
  "area_m2": 75.5
}
## 📤 Ejemplo de Respuesta JSON Exitosa (201 Created)

{
  "success": true,
  "statusCode": 201,
  "message": "Inmueble registrado exitosamente",
  "data": {
    "id_inmueble": 1,
    "numero": "101",
    "torre": "A",
    "area_m2": 75.5,
    "estado": "disponible",
    "fecha_registro": "2026-04-28T10:30:00Z"
  }
}

## 📤 Ejemplo de Respuesta JSON Error (400 Bad Request)
{
  "success": false,
  "statusCode": 400,
  "message": "Error en la solicitud",
  "error": {
    "error_code": "INMUEBLE_DUPLICADO",
    "details": "Ya existe un inmueble con el número 101 en la torre A",
    "timestamp": "2026-04-28T10:30:00Z"
  }
}

## 🧪 Requisitos de Pruebas
## 🔍 Casos de Prueba Funcional
### ✅ Caso 1: Registro exitoso de inmueble
- Precondición: Usuario autenticado es administrador. No existe inmueble "101" en torre "A".
- Acción: Ejecutar POST /api/v1/inmuebles con los datos de ejemplo.
- Resultado esperado:
- Código HTTP 201 Created
- success: true
- data.id_inmueble contiene un número
- data.estado = "disponible"
- El inmueble se guarda en la base de datos

### ❌ Caso 2: Inmueble duplicado (mismo número y torre)
- Precondición: Ya existe un inmueble con número "101" en torre "A".
- Acción: Enviar POST /api/v1/inmuebles con mismo número y torre.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: INMUEBLE_DUPLICADO

### ❌ Caso 3: Área inválida (cero o negativa)
- Precondición: Usuario autenticado es administrador.
- Acción: Enviar POST /api/v1/inmuebles con area_m2 = 0.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: AREA_INVALIDA

### ❌ Caso 4: Campo obligatorio faltante
- Precondición: Usuario autenticado es administrador.
- Acción: Enviar POST /api/v1/inmuebles sin el campo torre.
- Resultado esperado:
- Código HTTP 400 Bad Request
- success: false
- error.error_code: CAMPO_REQUERIDO

### ❌ Caso 5:Usuario no autenticado
- Precondición: El cliente no envía token de autenticación.
- Acción: Enviar POST /api/v1/inmuebles sin header Authorization.
- Resultado esperado:
- Código HTTP 401 Unauthorized
- success: false
- error.error_code: NO_AUTENTICADO

### ❌ Caso 6: Usuario autenticado no es administrador
- Precondición: El token pertenece a un usuario con id_rol = 2 (residente).
- Acción: Enviar POST /api/v1/inmuebles con el token de residente.
- Resultado esperado:
- Código HTTP 403 Forbidden
- success: false
- error.error_code: ACCESO_DENEGADO

## ✅ Caso 7: Verificar estado inicial
- Precondición: Usuario autenticado es administrador.
- Acción: Registrar un nuevo inmueble exitosamente.
- Resultado esperado:
- El campo estado en la base de datos es "disponible"
- El campo fecha_registro contiene la fecha y hora actual

## ✅ Definición de Hecho
- Historia: [HU-004] Registro de inmuebles
## 📦 Alcance Funcional
- [ ] El endpoint POST /api/v1/inmuebles está implementado.
- [ ] Las validaciones de campos obligatorios funcionan.
- [ ] La validación de unicidad (número + torre) funciona.
- [ ] La validación de área positiva funciona.
- [ ] La validación de autenticación y permisos funciona (solo administradores).
- [ ] El estado inicial "disponible" se asigna automáticamente.
- [ ] Las respuestas JSON cumplen con el contrato definido.

## 🧪 Pruebas Completadas
- [ ] Se ejecutaron pruebas unitarias para cada validación.
- [ ] Se ejecutaron pruebas de integración para el flujo completo.
- [ ] Se probaron todos los casos de error documentados.
- [ ] Se verificó la unicidad de número por torre.

## 📄 Documentación Técnica
- [ ] Endpoint documentado en Swagger / OpenAPI.
- [ ] Se describe: propósito del endpoint, campos de entrada y salida.
- [ ] Ejemplo de respuesta exitosa y de error.

## 🔐 Manejo de Errores
- [ ] Se devuelve código HTTP 400 para errores de validación.
- [ ] Se devuelve código HTTP 401 para usuario no autenticado.
- [ ] Se devuelve código HTTP 403 para permisos insuficientes.
- [ ] El campo error en el JSON incluye error_code, details y timestamp.
- [ ] No se devuelve información sensible en los errores.