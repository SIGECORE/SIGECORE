# app/api/v1/comunicados.py
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from datetime import datetime
import jwt

from domain.models_domain import ComunicadoCreate, ComunicadoResponse
from service.comunicado_service import ComunicadoService
from repository.comunicado_repository import ComunicadoRepository


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


router = APIRouter(tags=["Comunicados"])


@router.post("/comunicados", response_model=ComunicadoResponse, status_code=201)
def publicar_comunicado(
    data: ComunicadoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Solo administradores pueden publicar comunicados
    if usuario.get('id_rol') != 1:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Permiso denegado",
                "error": {
                    "error_code": "AUTOR_NO_AUTORIZADO",
                    "details": "Solo administradores pueden publicar comunicados",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    comunicado_repo = ComunicadoRepository()
    comunicado_service = ComunicadoService(comunicado_repo)
    
    return comunicado_service.publicar_comunicado(data, usuario)


@router.get("/comunicados", response_model=list[ComunicadoResponse])
def listar_comunicados_activos(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    comunicado_repo = ComunicadoRepository()
    comunicado_service = ComunicadoService(comunicado_repo)
    
    return comunicado_service.listar_comunicados_activos()