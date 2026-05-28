# app/api/v1/router.py
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import jwt

from database import get_db
from schemas import AsignarPropietarioRequest, InmuebleResponse
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


@router.patch("/{inmueble_id}/propietario", response_model=InmuebleResponse)
def asignar_propietario(
    inmueble_id: int, 
    data: AsignarPropietarioRequest, 
    request: Request, 
    db: Session = Depends(get_db)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail="Token de autenticación requerido"
        )
    
    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    usuario = validar_token(token)
    
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )
    
    repo = InmuebleRepository(db)
    service = InmuebleService(repo)
    return service.asignar_propietario(inmueble_id, data.id_propietario, usuario)
