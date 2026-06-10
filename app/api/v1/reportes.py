from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
import jwt
from pydantic import BaseModel

SECRET_KEY = "mi_clave_secreta"
security = HTTPBearer()


class ReporteCreate(BaseModel):
    tipo: str
    descripcion: str
    evidencias: Optional[List[str]] = []


def validar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id_usuario": payload.get("id_usuario"),
            "nombre_completo": payload.get("nombre_completo"),
            "email": payload.get("email"),
            "id_rol": payload.get("id_rol")
        }
    except Exception as e:
        print(f"Error validando token: {e}")
        return None


# Repositorio en memoria
reportes_db = {}
next_id = 1

router = APIRouter(tags=["Reportes"])


@router.post("/reportes", status_code=status.HTTP_201_CREATED)
def crear_reporte(
    data: ReporteCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    global next_id, reportes_db
    
    # Validar token
    token = credentials.credentials
    usuario = validar_token(token)
    
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    # Validar tipo
    if not data.tipo:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "CAMPO_REQUERIDO",
                    "details": "El campo tipo es obligatorio",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    tipos_validos = ["daño", "queja", "solicitud"]
    if data.tipo not in tipos_validos:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "TIPO_INVALIDO",
                    "details": "El tipo debe ser: daño, queja o solicitud",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    # Validar descripcion
    if not data.descripcion or data.descripcion.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "CAMPO_REQUERIDO",
                    "details": "El campo descripcion es obligatorio",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    # Obtener nombre del usuario
    nombre_usuario = usuario.get('nombre_completo')
    if not nombre_usuario:
        nombre_usuario = f"Usuario {usuario.get('id_usuario')}"
    
    # Crear reporte
    reporte = {
        "id_reporte": next_id,
        "id_usuario": usuario.get('id_usuario'),
        "nombre_usuario": nombre_usuario,
        "tipo": data.tipo,
        "descripcion": data.descripcion,
        "evidencias": data.evidencias if data.evidencias else [],
        "estado": "pendiente",
        "fecha_reporte": datetime.now()
    }
    
    reportes_db[next_id] = reporte
    next_id += 1
    
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Reporte creado exitosamente",
            "data": {
                "id_reporte": reporte["id_reporte"],
                "id_usuario": reporte["id_usuario"],
                "nombre_usuario": reporte["nombre_usuario"],
                "tipo": reporte["tipo"],
                "descripcion": reporte["descripcion"],
                "evidencias": reporte["evidencias"],
                "estado": reporte["estado"],
                "fecha_reporte": reporte["fecha_reporte"].isoformat()
            }
        }
    )

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel


class ActualizarEstadoRequest(BaseModel):
    estado: str
    observaciones: Optional[str] = None
    id_responsable: Optional[int] = None


@router.patch("/reportes/{reporte_id}/estado", status_code=status.HTTP_200_OK)
def actualizar_estado_reporte(
    reporte_id: int,
    data: ActualizarEstadoRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    global reportes_db
    
    # Validar token
    token = credentials.credentials
    usuario = validar_token(token)
    
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Validar que sea administrador
    if usuario.get('id_rol') != 1:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "ACCESO_DENEGADO",
                    "details": "Se requiere rol de administrador para actualizar el estado de reportes",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Validar que el reporte existe
    if reporte_id not in reportes_db:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "statusCode": 404,
                "message": "Reporte no encontrado",
                "error": {
                    "error_code": "REPORTE_NOT_FOUND",
                    "details": f"No existe un reporte con el ID {reporte_id}",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Validar estado válido
    estados_validos = ["en_proceso", "resuelto"]
    if data.estado not in estados_validos:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ESTADO_INVALIDO",
                    "details": "El estado debe ser: en_proceso o resuelto",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    reporte = reportes_db[reporte_id]
    
    # Validar que el responsable existe (si se envía)
    responsable_nombre = None
    if data.id_responsable:
        # Buscar responsable en la base de datos de usuarios
        # Por ahora usamos una búsqueda simple
        from repository.usuario_repository import UsuarioRepository
        usuario_repo = UsuarioRepository()
        responsable = usuario_repo.get_by_id(data.id_responsable)
        
        if not responsable:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Responsable no encontrado",
                    "error": {
                        "error_code": "RESPONSABLE_NOT_FOUND",
                        "details": f"No existe un usuario con el ID {data.id_responsable}",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
        responsable_nombre = responsable.get('nombre_completo')
    
    # Actualizar reporte
    reporte["estado"] = data.estado
    reporte["observaciones"] = data.observaciones
    reporte["fecha_actualizacion"] = datetime.now(timezone.utc)
    
    if data.id_responsable:
        reporte["id_responsable"] = data.id_responsable
        reporte["responsable_nombre"] = responsable_nombre
    
    if data.estado == "resuelto":
        reporte["fecha_resolucion"] = datetime.now(timezone.utc)
    
    # Construir respuesta
    response_data = {
        "id_reporte": reporte["id_reporte"],
        "estado": reporte["estado"],
        "observaciones": reporte.get("observaciones"),
        "fecha_actualizacion": reporte["fecha_actualizacion"].isoformat(),
        "fecha_resolucion": reporte.get("fecha_resolucion").isoformat() if reporte.get("fecha_resolucion") else None
    }
    
    if data.id_responsable:
        response_data["responsable"] = {
            "id_responsable": data.id_responsable,
            "nombre": responsable_nombre,
            "cargo": "Mantenimiento"
        }
    
    mensaje = "Reporte resuelto exitosamente" if data.estado == "resuelto" else "Estado del reporte actualizado exitosamente"
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": mensaje,
            "data": response_data
        }
    )