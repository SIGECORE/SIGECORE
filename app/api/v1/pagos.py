# app/api/v1/pagos.py
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from domain.models_domain import (
    PagoRequest,
    PagoResponse,
    HistorialPagosResponse,
    ReporteCarteraResponse
)
from service.pago_service import PagoService
from service.reporte_service import ReporteService
from repository.inmueble_repository import InmuebleRepository
from repository.pago_repository import PagoRepository


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

router = APIRouter(tags=["Pagos"])


@router.post("/pagos", response_model=PagoResponse, status_code=201)
def registrar_pago(data: PagoRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    pago_service = PagoService(pago_repo, inmueble_repo)
    return pago_service.registrar_pago(data, usuario)


@router.get("/pagos/usuario/{usuario_id}", response_model=HistorialPagosResponse)
def obtener_historial_pagos(usuario_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    pago_service = PagoService(pago_repo, inmueble_repo)
    return pago_service.obtener_historial_pagos(usuario_id, usuario)


@router.get("/pagos/reporte-cartera", response_model=ReporteCarteraResponse)
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