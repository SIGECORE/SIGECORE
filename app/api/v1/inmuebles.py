# app/api/v1/inmuebles.py
from typing import Optional
from fastapi import APIRouter, status, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from domain.models_domain import (
    InmuebleCreate,
    InmuebleResponse,
    ListaInmueblesResponse,
    AsignarPropietarioRequest
)
from service.inmueble_service import InmuebleService
from repository.inmueble_repository import InmuebleRepository


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


inmueble_repo = InmuebleRepository()
inmueble_service = InmuebleService(inmueble_repo)

router = APIRouter(tags=["Inmuebles"])


@router.post("/inmuebles", response_model=InmuebleResponse, status_code=status.HTTP_201_CREATED)
def create_inmueble(data: InmuebleCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
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
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return inmueble_service.listar_inmuebles(torre, estado, nombre_propietario, page, limit)


@router.patch("/inmuebles/{inmueble_id}/propietario", response_model=InmuebleResponse)
def asignar_propietario(
    inmueble_id: int,
    data: AsignarPropietarioRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return inmueble_service.asignar_propietario(inmueble_id, data.id_propietario, usuario)