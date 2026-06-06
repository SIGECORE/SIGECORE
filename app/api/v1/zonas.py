# app/api/v1/zonas.py
from fastapi import APIRouter, status, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from domain.models_domain import ZonaCreate, ZonaResponse, DisponibilidadResponse
from service.zona_service import ZonaService
from service.disponibilidad_service import DisponibilidadService
from repository.zona_repository import ZonaRepository
from repository.reserva_repository import ReservaRepository


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


zona_repo = ZonaRepository()
reserva_repo = ReservaRepository()
zona_service = ZonaService(zona_repo)

router = APIRouter(tags=["Zonas Comunes"])


@router.post("/zonas", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED)
def crear_zona(data: ZonaCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return zona_service.registrar_zona(data, usuario)


@router.get("/zonas/disponibilidad", response_model=DisponibilidadResponse)
def consultar_disponibilidad(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    zona_id: int = Query(..., description="ID de la zona común"),
    fecha: str = Query(..., description="Fecha (YYYY-MM-DD)"),
    hora_inicio: str = Query(..., description="Hora inicio (HH:MM)"),
    hora_fin: str = Query(..., description="Hora fin (HH:MM)")
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    from datetime import datetime
    try:
        fecha_actual = datetime.now().date()
        fecha_consulta = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_consulta < fecha_actual:
            raise HTTPException(status_code=400, detail="La fecha no puede ser anterior a la fecha actual")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
    
    if hora_inicio >= hora_fin:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor que la hora de fin")
    
    service = DisponibilidadService(zona_repo, reserva_repo)
    return service.consultar_disponibilidad(usuario, zona_id, fecha, hora_inicio, hora_fin)