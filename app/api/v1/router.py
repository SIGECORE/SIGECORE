# app/api/v1/router.py
from fastapi import APIRouter, status, Request, HTTPException
import jwt

from domain.models_domain import ZonaCreate, ZonaResponse
from service.zona_service import ZonaService
from repository.zona_repository import ZonaRepository


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


zona_repo = ZonaRepository()
zona_service = ZonaService(zona_repo)

router = APIRouter(prefix="/zonas", tags=["Zonas Comunes"])


@router.post("/", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED)
def registrar_zona(data: ZonaCreate, request: Request):
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
    
    return zona_service.registrar_zona(data, usuario)