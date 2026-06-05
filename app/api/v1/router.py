# app/api/v1/router.py
from typing import Optional
from fastapi import APIRouter, status, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from domain.models_domain import (
    InmuebleCreate,
    InmuebleResponse,
    ListaInmueblesResponse,
    AsignarPropietarioRequest,
    PagoRequest,
    PagoResponse
)
from service.inmueble_service import InmuebleService
from service.pago_service import PagoService
from repository.inmueble_repository import InmuebleRepository
from repository.pago_repository import PagoRepository


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


# Repositorios y servicios (compartidos)
inmueble_repo = InmuebleRepository()
inmueble_service = InmuebleService(inmueble_repo)

router = APIRouter()


# ==================== HU-004 (Registro de inmuebles) ====================
@router.post("/inmuebles", response_model=InmuebleResponse, status_code=status.HTTP_201_CREATED)
def create_inmueble(data: InmuebleCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol de administrador")
    
    return inmueble_service.create_inmueble(data, usuario)


# ==================== HU-006 (Consulta de inmuebles) ====================
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
    
    return inmueble_service.listar_inmuebles(torre, estado, nombre_propietario, page, limit)


# ==================== HU-005 (Asignación de propietario) ====================
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
        raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere rol de administrador")
    
    return inmueble_service.asignar_propietario(inmueble_id, data.id_propietario, usuario)


# ==================== HU-015 (Registro de pago) ====================
@router.post("/pagos", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pago(
    data: PagoRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Token de autenticación requerido")
    
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # resto del código...