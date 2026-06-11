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


@router.get("/pagos/reporte-cartera")
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

@router.post("/pagos/debug/crear-datos-prueba")
def crear_datos_prueba(credentials: HTTPAuthorizationCredentials = Depends(security)):
    from repositories import inmueble_repo, pago_repo
    from domain.models_domain import InmuebleCreate, PagoResponse
    from datetime import datetime, timedelta
    
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    # Limpiar datos existentes
    inmueble_repo._db.clear()
    inmueble_repo._next_id = 1
    pago_repo._db.clear()
    pago_repo._next_id = 1
    
    # Crear inmuebles
    i1 = inmueble_repo.create(InmuebleCreate(numero='101', torre='A', area_m2=75.5))
    i1.id_propietario = 1
    
    i2 = inmueble_repo.create(InmuebleCreate(numero='102', torre='A', area_m2=85.0))
    i2.id_propietario = 2
    
    i3 = inmueble_repo.create(InmuebleCreate(numero='201', torre='B', area_m2=95.0))
    i3.id_propietario = 2
    
    # Crear pagos con fechas antiguas
    # Pago para inmueble 1 (hace 4 meses)
    pago1 = PagoResponse(
        id_pago=1,
        id_usuario=1,
        id_inmueble=1,
        monto=150000,
        metodo_pago='tarjeta',
        estado='confirmado',
        fecha_pago=datetime.now() - timedelta(days=120),
        comprobante_url='/recibo.pdf'
    )
    pago_repo._db[1] = pago1
    pago_repo._next_id = 2
    
    # Pago para inmueble 2 (hace 2 meses)
    pago2 = PagoResponse(
        id_pago=2,
        id_usuario=2,
        id_inmueble=2,
        monto=150000,
        metodo_pago='tarjeta',
        estado='confirmado',
        fecha_pago=datetime.now() - timedelta(days=60),
        comprobante_url='/recibo.pdf'
    )
    pago_repo._db[2] = pago2
    pago_repo._next_id = 3
    
    # Inmueble 3 no tiene pagos (moroso de 6 meses)
    
    return {
        "message": "Datos creados: morosos con 2, 4 y 6 meses",
        "inmuebles": len(inmueble_repo._db),
        "pagos": len(pago_repo._db)
    }

@router.get("/pagos/debug/verificar-inmuebles")
def verificar_inmuebles(credentials: HTTPAuthorizationCredentials = Depends(security)):
    from repositories import inmueble_repo
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    return {
        "db_directo": {k: {"id": v.id_inmueble, "propietario": v.id_propietario} for k, v in inmueble_repo._db.items()},
        "get_all_inmuebles": [(i.id_inmueble, i.id_propietario) for i in inmueble_repo.get_all_inmuebles()]
    }