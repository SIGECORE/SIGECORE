# app/api/v1/router.py
from fastapi import APIRouter, status, Request, HTTPException
import jwt

from domain.models_domain import Inmueble, AsignarPropietarioRequest
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

router = APIRouter(prefix="/inmuebles", tags=["inmuebles"])


@router.patch("/{inmueble_id}/propietario", response_model=Inmueble, status_code=status.HTTP_200_OK)
def asignar_propietario(inmueble_id: int, data: AsignarPropietarioRequest, request: Request):
    
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
    
    return service.asignar_propietario(inmueble_id, data.id_propietario, usuario)