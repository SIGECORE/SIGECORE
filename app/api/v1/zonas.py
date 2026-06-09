# app/api/v1/zonas.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from domain.models_domain import ZonaCreate, ZonaResponse
from repositories import zona_repo

router = APIRouter(tags=["Zonas Comunes"])

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


@router.post("/zonas", response_model=ZonaResponse, status_code=201)
def crear_zona(data: ZonaCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return zona_repo.create(data)


@router.get("/zonas")
def listar_zonas(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return zona_repo.get_all()