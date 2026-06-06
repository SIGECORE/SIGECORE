from datetime import datetime

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)

from fastapi.responses import JSONResponse

import jwt

from domain.models_domain import (
    ReporteCreate,
    ActualizarEstadoReporteRequest
)

from repository.reporte_repository import ReporteRepository
from repository.usuario_repository import UsuarioRepository

from service.reporte_service import ReporteService


SECRET_KEY = "mi_clave_secreta"


def validar_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return {
            "id_usuario": payload.get("id_usuario"),
            "nombre_completo": payload.get("nombre_completo"),
            "email": payload.get("email"),
            "id_rol": payload.get("id_rol")
        }

    except:

        return None


usuario_repository = UsuarioRepository()

reporte_repository = ReporteRepository()

service = ReporteService(
    reporte_repository,
    usuario_repository
)

router = APIRouter(
    prefix="/api/v1/reportes",
    tags=["reportes"]
)


# ==================================================
# HU-018 CREAR REPORTE
# ==================================================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def crear_reporte(
    data: ReporteCreate,
    request: Request
):

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:

        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    token = (
        auth_header.split(" ")[1]
        if " " in auth_header
        else auth_header
    )

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
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    reporte = service.crear_reporte(
        data,
        usuario
    )

    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Reporte creado exitosamente",
            "data": {
                "id_reporte": reporte.id_reporte,
                "id_usuario": reporte.id_usuario,
                "nombre_usuario": reporte.nombre_usuario,
                "tipo": reporte.tipo,
                "descripcion": reporte.descripcion,
                "evidencias": reporte.evidencias,
                "estado": reporte.estado,
                "fecha_reporte": reporte.fecha_reporte.isoformat()
            }
        }
    )


# ==================================================
# HU-019 ACTUALIZAR ESTADO
# ==================================================

@router.patch(
    "/{id_reporte}/estado",
    status_code=status.HTTP_200_OK
)
def actualizar_estado_reporte(
    id_reporte: int,
    data: ActualizarEstadoReporteRequest,
    request: Request
):

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:

        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    token = (
        auth_header.split(" ")[1]
        if " " in auth_header
        else auth_header
    )

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
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    resultado = service.actualizar_estado(
        id_reporte,
        data,
        usuario
    )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": (
                "Reporte resuelto exitosamente"
                if resultado["estado"] == "resuelto"
                else "Estado del reporte actualizado exitosamente"
            ),
            "data": resultado
        }
    )