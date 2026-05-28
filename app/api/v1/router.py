# app/api/v1/router.py
from typing import Optional
from fastapi import APIRouter, status, Request, HTTPException, Depends, Query
from sqlalchemy.orm import Session
import jwt

from database import get_db
from schemas import ListaInmueblesResponse
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


router = APIRouter(prefix="/inmuebles", tags=["inmuebles"])


# SOLO EL MÉTODO GET PARA HU-006
@router.get("/", response_model=ListaInmueblesResponse)
def listar_inmuebles(
    request: Request,
    torre: Optional[str] = Query(None, description="Filtrar por torre"),
    estado: Optional[str] = Query(None, description="Filtrar por estado (disponible, ocupado, mantenimiento)"),
    nombre_propietario: Optional[str] = Query(None, description="Filtrar por nombre del propietario"),
    page: int = Query(1, ge=1, description="Número de página"),
    limit: int = Query(10, ge=1, le=100, description="Elementos por página"),
    db: Session = Depends(get_db)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido"
        )
    
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    usuario = validar_token(token)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    repo = InmuebleRepository(db)
    service = InmuebleService(repo)
    return service.listar_inmuebles(usuario, torre, estado, nombre_propietario, page, limit)