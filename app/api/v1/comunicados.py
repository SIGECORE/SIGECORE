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


# ==================== HU-013 (Publicación de comunicados) ====================
@router.post("/comunicados", response_model=ComunicadoResponse, status_code=201)
def publicar_comunicado(
    data: ComunicadoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
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


# ==================== HU-014 (Consulta de comunicados activos) ====================
@router.get("/comunicados/activos", tags=["Comunicados"])
def listar_comunicados_activos(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
                    "timestamp": datetime.now().isoformat()
                }
            }
        )
    
    comunicado_repo = ComunicadoRepository()
    comunicado_service = ComunicadoService(comunicado_repo)
    
    comunicados = comunicado_service.listar_comunicados_activos()
    
    if not comunicados:
        return {
            "success": True,
            "statusCode": 200,
            "message": "No hay comunicados activos en este momento",
            "data": {
                "comunicados": []
            }
        }
    
    return {
        "success": True,
        "statusCode": 200,
        "message": "Consulta exitosa",
        "data": {
            "comunicados": [
                {
                    "id_comunicado": c.id_comunicado,
                    "titulo": c.titulo,
                    "contenido": c.contenido,
                    "autor": {
                        "id_autor": c.id_autor,
                        "nombre": c.autor_nombre
                    },
                    "archivos_adjuntos": c.archivos_adjuntos,
                    "fecha_publicacion": c.fecha_publicacion.isoformat()
                }
                for c in comunicados
            ]
        }
    }