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
    ReporteCreate
)

from repository.reporte_repository import (
    ReporteRepository
)

from service.reporte_service import (
    ReporteService
)


SECRET_KEY = "mi_clave_secreta"


def validar_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return {
            "id_usuario": payload.get("id_usuario"),
            "nombre_completo": payload.get(
                "nombre_completo"
            ),
            "email": payload.get(
                "email"
            ),
            "id_rol": payload.get(
                "id_rol"
            )
        }

    except Exception:

        return None


repo = ReporteRepository()

service = ReporteService(
    repo
)


router = APIRouter(
    prefix="/api/v1/reportes",
    tags=["reportes"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Crear Reporte"
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

    usuario = validar_token(
        token
    )

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
                "id_reporte": reporte["id_reporte"],
                "id_usuario": reporte["id_usuario"],
                "nombre_usuario": reporte["nombre_usuario"],
                "tipo": reporte["tipo"],
                "descripcion": reporte["descripcion"],
                "evidencias": reporte["evidencias"],
                "estado": reporte["estado"],
                "fecha_reporte": reporte[
                    "fecha_reporte"
                ].isoformat()
            }
        }
    )