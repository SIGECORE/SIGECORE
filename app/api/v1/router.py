# app/api/v1/router.py
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import jwt

from database import get_db
from domain.models_domain import HistorialPagosResponse
from service.pago_service import PagoService
from repository.pago_repository import PagoRepository
from repository.usuario_repository import UsuarioRepository


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


router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.get("/usuario/{usuario_id}", response_model=HistorialPagosResponse)
def obtener_historial_pagos(
    usuario_id: int, 
    request: Request, 
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
    
    pago_repo = PagoRepository(db)
    usuario_repo = UsuarioRepository(db)
    service = PagoService(pago_repo, usuario_repo)
    
    return service.obtener_historial_pagos(usuario_id, usuario)