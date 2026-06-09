# app/api/v1/reservas.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
import jwt

from domain.models_domain import ReservaCreate, ReservaResponse
from service.reserva_service import ReservaService
from repositories import reserva_repo, zona_repo, usuario_repo


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


router = APIRouter(tags=["Reservas"])


@router.post("/reservas", response_model=ReservaResponse, status_code=201)
def solicitar_reserva(
    data: ReservaCreate,
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
    
    reserva_service = ReservaService(reserva_repo, zona_repo, usuario_repo)
    
    return reserva_service.solicitar_reserva(data, usuario)


@router.delete("/reservas/{reserva_id}")
def cancelar_reserva(
    reserva_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    reserva_service = ReservaService(reserva_repo, zona_repo, usuario_repo)
    
    return reserva_service.cancelar_reserva(reserva_id, usuario)