# app/api/v1/router.py
from fastapi import APIRouter, status, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import jwt

from database import get_db
from schemas import PagoRequest, PagoResponse
from service.pago_service import PagoService
from repository.pago_repository import PagoRepository
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


router = APIRouter(prefix="/pagos", tags=["pagos"])


@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pago(data: PagoRequest, request: Request, db: Session = Depends(get_db)):
    
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
    inmueble_repo = InmuebleRepository(db)
    service = PagoService(pago_repo, inmueble_repo)
    return service.registrar_pago(data, usuario)