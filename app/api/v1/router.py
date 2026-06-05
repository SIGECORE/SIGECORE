# app/api/v1/router.py
from typing import Optional
from fastapi import APIRouter, status, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from domain.models_domain import InmuebleCreate, InmuebleResponse, ListaInmueblesResponse
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


repo = InmuebleRepository()
service = InmuebleService(repo)

router = APIRouter()


@router.post("/inmuebles", response_model=InmuebleResponse, status_code=status.HTTP_201_CREATED)
def create_inmueble(data: InmuebleCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol de administrador")
    
    return service.create_inmueble(data, usuario)


@router.get("/inmuebles", response_model=ListaInmueblesResponse)
def listar_inmuebles(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    torre: str = Query(None, description="Filtrar por torre"),
    estado: str = Query(None, description="Filtrar por estado"),
    nombre_propietario: str = Query(None, description="Filtrar por nombre del propietario"),
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Elementos por página")
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol de administrador")
    
    return service.listar_inmuebles(torre, estado, nombre_propietario, page, limit)