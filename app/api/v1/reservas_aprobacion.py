# app/api/v1/reservas_aprobacion.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
import jwt

from domain.models_domain import AprobarReservaRequest
from service.reserva_aprobacion_service import ReservaAprobacionService
from repositories import reserva_repo


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


@router.get("/reservas/pendientes")
def listar_reservas_pendientes(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    service = ReservaAprobacionService(reserva_repo)
    pendientes = service.listar_pendientes(usuario)
    
    return {
        "success": True,
        "statusCode": 200,
        "message": "Consulta exitosa",
        "data": {
            "pendientes": [
                {
                    "id_reserva": r.id_reserva,
                    "solicitante": {
                        "id_usuario": r.id_usuario,
                        "nombre": r.nombre_usuario,
                        "email": f"usuario{r.id_usuario}@example.com",
                        "telefono": "3000000000"
                    },
                    "zona": {
                        "id_zona": r.id_zona,
                        "nombre": r.nombre_zona
                    },
                    "fecha": r.fecha,
                    "hora_inicio": r.hora_inicio,
                    "hora_fin": r.hora_fin,
                    "observaciones": "",
                    "fecha_solicitud": r.fecha_solicitud.isoformat()
                }
                for r in pendientes
            ]
        }
    }


@router.patch("/reservas/{reserva_id}/estado")
def aprobar_rechazar_reserva(
    reserva_id: int,
    data: AprobarReservaRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    service = ReservaAprobacionService(reserva_repo)
    return service.aprobar_rechazar(reserva_id, data, usuario)