# app/api/v1/router.py
from typing import Optional
from fastapi import APIRouter, status, Request, HTTPException, Query
import jwt

from domain.models_domain import InmuebleCreate, InmuebleResponse, ListaInmueblesResponse
from service.inmueble_service import InmuebleService
from repository.inmueble_repository import InmuebleRepository


SECRET_KEY = "mi_clave_secreta"

def validar_token(token: str) -> dict:
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


# ==================== HU-004 (Registro de inmuebles) ====================
@router.post("/inmuebles", response_model=InmuebleResponse, status_code=status.HTTP_201_CREATED)
def create_inmueble(data: InmuebleCreate, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Token requerido")
    
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return service.create_inmueble(data, usuario)


# ==================== HU-006 (Consulta de inmuebles) ====================
@router.get("/inmuebles", response_model=ListaInmueblesResponse)
def listar_inmuebles(
    torre: Optional[str] = Query(None),
    estado: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    return service.listar_inmuebles(torre, estado, page, limit)