# app/api/v1/pagos.py
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from datetime import datetime
import jwt

from domain.models_domain import (
    PagoRequest,
    PagoResponse,
    HistorialPagosResponse,
    ReporteCarteraResponse
)
from service.pago_service import PagoService
from repositories import pago_repo, inmueble_repo, usuario_repo


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


pago_service = PagoService(pago_repo, inmueble_repo, usuario_repo)

router = APIRouter(tags=["Pagos"])


@router.post("/pagos", response_model=PagoResponse, status_code=201)
def registrar_pago(
    data: PagoRequest,
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
    
    return pago_service.registrar_pago(data, usuario)


@router.get("/pagos/usuario/{usuario_id}", response_model=HistorialPagosResponse)
def obtener_historial_pagos(
    usuario_id: int,
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
    
    return pago_service.obtener_historial_pagos(usuario_id, usuario)


@router.get("/pagos/reporte-cartera", response_model=ReporteCarteraResponse)
def reporte_cartera(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    torre: str = Query(None, description="Filtrar por torre"),
    meses_mora: int = Query(None, description="Filtrar por meses de mora mínimos")
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
    
    return pago_service.generar_reporte_cartera(usuario, torre, meses_mora)


@router.get("/pagos/debug/inmuebles")
def debug_inmuebles_pagos(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    usuario = validar_token(token)
    
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return {
        "inmuebles_en_repo": [(k, v.numero, v.torre, v.id_propietario) for k, v in inmueble_repo._db.items()]
    }