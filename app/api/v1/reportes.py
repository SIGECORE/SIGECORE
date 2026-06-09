# app/api/v1/reportes.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
import jwt

from domain.models_domain import ReporteCreate, ReporteResponse, ActualizarReporteRequest
from service.reporte_service import ReporteService
from repository.reporte_repository import ReporteRepository


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


router = APIRouter(tags=["Reportes"])


@router.get("/reportes", tags=["Reportes"])
def listar_reportes(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    reporte_repo = ReporteRepository()
    return reporte_repo.get_all()


@router.post("/reportes", response_model=ReporteResponse, status_code=201)
def crear_reporte(
    data: ReporteCreate,
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
    
    reporte_repo = ReporteRepository()
    reporte_service = ReporteService(reporte_repo)
    
    return reporte_service.crear_reporte(data, usuario)


@router.patch("/reportes/{reporte_id}/estado", response_model=ReporteResponse)
def actualizar_estado_reporte(
    reporte_id: int,
    data: ActualizarReporteRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    reporte_repo = ReporteRepository()
    reporte_service = ReporteService(reporte_repo)
    
    return reporte_service.actualizar_estado(reporte_id, data, usuario)