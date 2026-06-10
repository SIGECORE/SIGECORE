from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
import jwt
from pydantic import BaseModel

SECRET_KEY = "mi_clave_secreta"
security = HTTPBearer()

# Usar el repositorio global
from repositories import zona_repo
from domain.models_domain import ZonaCreate, ZonaResponse


def validar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id_usuario": payload.get("id_usuario"),
            "id_rol": payload.get("id_rol")
        }
    except Exception:
        return None


router = APIRouter(tags=["Zonas Comunes"])


class ZonaCreateManual(BaseModel):
    nombre: str
    capacidad_maxima: int
    descripcion: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None
    estado: Optional[str] = "disponible"


@router.post("/zonas", status_code=status.HTTP_201_CREATED)
def registrar_zona(
    data: ZonaCreateManual,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
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
    
    if usuario.get('id_rol') != 1:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "ACCESO_DENEGADO",
                    "details": "Se requiere rol de administrador para registrar zonas comunes",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    if not data.nombre or data.nombre.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "CAMPO_REQUERIDO",
                    "details": "El campo nombre es obligatorio",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    if data.capacidad_maxima <= 0:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "CAPACIDAD_INVALIDA",
                    "details": "La capacidad máxima debe ser un número entero mayor a 0",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Validar nombre único usando el repositorio global
    for zona in zona_repo.get_all():
        if zona.nombre.lower() == data.nombre.lower():
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "ZONA_DUPLICADA",
                        "details": f"Ya existe una zona común con el nombre '{data.nombre}'",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    
    # Validar estado permitido
    if data.estado not in ["disponible", "mantenimiento"]:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ESTADO_INVALIDO",
                    "details": "El estado debe ser 'disponible' o 'mantenimiento'",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Crear zona usando el repositorio global
    zona_data = ZonaCreate(
        nombre=data.nombre,
        capacidad_maxima=data.capacidad_maxima,
        descripcion=data.descripcion,
        horario_inicio=data.horario_inicio,
        horario_fin=data.horario_fin
    )
    
    zona = zona_repo.create(zona_data)
    zona.estado = data.estado  # Sobrescribir estado si es mantenimiento
    
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Zona común registrada exitosamente",
            "data": {
                "id_zona": zona.id_zona,
                "nombre": zona.nombre,
                "capacidad_maxima": zona.capacidad_maxima,
                "descripcion": zona.descripcion,
                "estado": zona.estado,
                "horario_inicio": zona.horario_inicio,
                "horario_fin": zona.horario_fin,
                "fecha_registro": zona.fecha_registro.isoformat()
            }
        }
    )


@router.get("/zonas")
def listar_zonas(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado"
            }
        )
    
    zonas = []
    for zona in zona_repo.get_all():
        zonas.append({
            "id_zona": zona.id_zona,
            "nombre": zona.nombre,
            "capacidad_maxima": zona.capacidad_maxima,
            "descripcion": zona.descripcion,
            "estado": zona.estado,
            "horario_inicio": zona.horario_inicio,
            "horario_fin": zona.horario_fin,
            "fecha_registro": zona.fecha_registro.isoformat()
        })
    
    return {"zonas": zonas}


@router.get("/zonas/disponibilidad")
def consultar_disponibilidad(
    zona_id: int,
    fecha: str,
    hora_inicio: str,
    hora_fin: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
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
    
    # Validar que la zona existe
    zona = zona_repo.get_by_id(zona_id)
    if not zona:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "statusCode": 404,
                "message": "Zona no encontrada",
                "error": {
                    "error_code": "ZONA_NOT_FOUND",
                    "details": f"No existe una zona común con el ID {zona_id}",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Validar que la zona esté disponible
    if zona.estado != "disponible":
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Zona no disponible",
                "error": {
                    "error_code": "ZONA_MANTENIMIENTO",
                    "details": "La zona común está actualmente en mantenimiento y no puede ser reservada",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Validar fecha no sea anterior a hoy
    try:
        fecha_consulta = datetime.strptime(fecha, "%Y-%m-%d").date()
        hoy = datetime.now(timezone.utc).date()
        if fecha_consulta < hoy:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "FECHA_INVALIDA",
                        "details": "No se pueden consultar fechas anteriores a la actual",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "FECHA_INVALIDA",
                    "details": "Formato de fecha inválido. Use YYYY-MM-DD",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Validar horario
    if hora_inicio >= hora_fin:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "HORARIO_INVALIDO",
                    "details": "La hora de inicio debe ser menor que la hora de fin",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    # Verificar conflictos con reservas existentes
    from repositories import reserva_repo
    conflicto = reserva_repo.hay_conflicto(zona_id, fecha, hora_inicio, hora_fin)
    
    if conflicto:
        return {
            "success": True,
            "statusCode": 200,
            "message": "La zona no está disponible en el horario solicitado",
            "data": {
                "zona_id": zona_id,
                "nombre": zona.nombre,
                "fecha": fecha,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "disponible": False
            }
        }
    
    return {
        "success": True,
        "statusCode": 200,
        "message": "La zona está disponible",
        "data": {
            "zona_id": zona_id,
            "nombre": zona.nombre,
            "fecha": fecha,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "disponible": True
        }
    }