# app/api/v1/inmuebles.py
from typing import Optional
from fastapi import APIRouter, status, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from datetime import datetime
import jwt

from domain.models_domain import InmuebleCreate, InmuebleResponse, ListaInmueblesResponse, AsignarPropietarioRequest
from service.inmueble_service import InmuebleService
from repositories import inmueble_repo  # ← USAR EL REPOSITORIO CENTRAL


SECRET_KEY = "mi_clave_secreta"
security = HTTPBearer()


def validar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id_usuario": payload.get("id_usuario"),
            "nombre_completo": payload.get("nombre_completo"),
            "email": payload.get("email"),
            "id_rol": payload.get("id_rol")
        }
    except:
        return None


inmueble_service = InmuebleService(inmueble_repo)  # ← USAR EL REPOSITORIO CENTRAL

router = APIRouter(tags=["Inmuebles"])


@router.post("/inmuebles", response_model=InmuebleResponse, status_code=status.HTTP_201_CREATED)
def create_inmueble(
    data: InmuebleCreate,
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
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    return inmueble_service.create_inmueble(data, usuario)


@router.get("/inmuebles", response_model=ListaInmueblesResponse)
def listar_inmuebles(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    torre: str = Query(None),
    estado: str = Query(None),
    nombre_propietario: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
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
                    "timestamp": datetime.now().isoformat()
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
                    "details": "Se requiere rol de administrador para listar inmuebles",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    return inmueble_service.listar_inmuebles(torre, estado, nombre_propietario, page, limit)


@router.patch("/inmuebles/{inmueble_id}/propietario")
def asignar_propietario(
    inmueble_id: int,
    data: AsignarPropietarioRequest,
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
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    inmueble = inmueble_service.asignar_propietario(inmueble_id, data.id_propietario, usuario)
    
    from repositories import usuario_repo
    propietario = usuario_repo.get_by_id(data.id_propietario)
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Propietario asignado exitosamente",
            "data": {
                "id_inmueble": inmueble.id_inmueble,
                "numero": inmueble.numero,
                "torre": inmueble.torre,
                "area_m2": inmueble.area_m2,
                "estado": inmueble.estado,
                "propietario": {
                    "id_propietario": propietario["id_usuario"],
                    "nombre_completo": propietario["nombre_completo"],
                    "email": propietario["email"],
                    "telefono": propietario["telefono"]
                }
            }
        }
    )