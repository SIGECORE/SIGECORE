# app/api/v1/router.py
from typing import Optional
from fastapi import APIRouter, status, Request, HTTPException, Depends, Query
from sqlalchemy.orm import Session
import jwt

from database import get_db
from domain.models_domain import ReporteCarteraResponse
from service.reporte_service import ReporteService
from repository.inmueble_repository import InmuebleRepository
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


@router.get("/reporte-cartera", response_model=ReporteCarteraResponse)
def reporte_cartera(
    request: Request,
    torre: Optional[str] = Query(None, description="Filtrar por torre"),
    meses_mora: Optional[int] = Query(None, description="Filtrar por meses de mora mínimos"),
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
    
    inmueble_repo = InmuebleRepository(db)
    pago_repo = PagoRepository(db)
    usuario_repo = UsuarioRepository(db)
    service = ReporteService(inmueble_repo, pago_repo, usuario_repo)
    
    return service.generar_reporte_cartera(usuario, torre, meses_mora)