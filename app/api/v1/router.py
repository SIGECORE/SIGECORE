# app/api/v1/router.py
from typing import Optional
from fastapi import APIRouter, status, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from domain.models_domain import (
    InmuebleCreate,
    InmuebleResponse,
    ListaInmueblesResponse,
    AsignarPropietarioRequest,
    PagoRequest,
    PagoResponse,
    HistorialPagosResponse,
    ReporteCarteraResponse,
    ZonaCreate,
    ZonaResponse,
    DisponibilidadResponse
)
from service.inmueble_service import InmuebleService
from service.pago_service import PagoService
from service.reporte_service import ReporteService
from service.zona_service import ZonaService
from service.disponibilidad_service import DisponibilidadService
from repository.inmueble_repository import InmuebleRepository
from repository.pago_repository import PagoRepository
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


inmueble_repo = InmuebleRepository()
pago_repo = PagoRepository()
zona_repo = ZonaRepository()
reserva_repo = ReservaRepository()
inmueble_service = InmuebleService(inmueble_repo)
zona_service = ZonaService(zona_repo)

router = APIRouter()


# ==================== INMUEBLES ====================
@router.post("/inmuebles", response_model=InmuebleResponse, status_code=status.HTTP_201_CREATED, tags=["Inmuebles"])
def create_inmueble(data: InmuebleCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return inmueble_service.create_inmueble(data, usuario)


@router.get("/inmuebles", response_model=ListaInmueblesResponse, tags=["Inmuebles"])
def listar_inmuebles(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    torre: str = Query(None),
    estado: str = Query(None),
    nombre_propietario: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return inmueble_service.listar_inmuebles(torre, estado, nombre_propietario, page, limit)


@router.patch("/inmuebles/{inmueble_id}/propietario", response_model=InmuebleResponse, tags=["Inmuebles"])
def asignar_propietario(
    inmueble_id: int,
    data: AsignarPropietarioRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return inmueble_service.asignar_propietario(inmueble_id, data.id_propietario, usuario)


# ==================== PAGOS ====================
@router.post("/pagos", response_model=PagoResponse, status_code=status.HTTP_201_CREATED, tags=["Pagos"])
def registrar_pago(data: PagoRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    pago_service = PagoService(pago_repo, inmueble_repo)
    return pago_service.registrar_pago(data, usuario)


@router.get("/pagos/usuario/{usuario_id}", response_model=HistorialPagosResponse, tags=["Pagos"])
def obtener_historial_pagos(usuario_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    pago_service = PagoService(pago_repo, inmueble_repo)
    return pago_service.obtener_historial_pagos(usuario_id, usuario)


@router.get("/pagos/reporte-cartera", response_model=ReporteCarteraResponse, tags=["Pagos"])
def reporte_cartera(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    torre: str = Query(None),
    meses_mora: int = Query(None)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    reporte_service = ReporteService(inmueble_repo, pago_repo)
    return reporte_service.generar_reporte_cartera(usuario, torre, meses_mora)


# ==================== ZONAS COMUNES ====================
@router.post("/zonas", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED, tags=["Zonas Comunes"])
def crear_zona(data: ZonaCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    if usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return zona_service.registrar_zona(data, usuario)


# ==================== HU-008 (Consulta de disponibilidad de zonas) ====================
@router.get("/zonas/disponibilidad", response_model=DisponibilidadResponse, tags=["Zonas Comunes"])
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
    
    # Validar fecha no pasada
    from datetime import datetime
    try:
        fecha_actual = datetime.now().date()
        fecha_consulta = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_consulta < fecha_actual:
            raise HTTPException(status_code=400, detail="La fecha no puede ser anterior a la fecha actual")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
    
    # Validar horario
    if hora_inicio >= hora_fin:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor que la hora de fin")
    
    # Validar parámetros obligatorios
    if not zona_id or not fecha or not hora_inicio or not hora_fin:
        raise HTTPException(status_code=400, detail="Todos los parámetros son obligatorios")
    
    service = DisponibilidadService(zona_repo, reserva_repo)
    return service.consultar_disponibilidad(usuario, zona_id, fecha, hora_inicio, hora_fin)