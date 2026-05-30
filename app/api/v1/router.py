from datetime import datetime

import jwt

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status
)

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.database import get_db

from app.domain.models_domain import (
    ReporteCreate
)

from app.repository.reporte_repository import (
    ReporteRepository
)

from app.service.reporte_service import (
    ReporteService
)


SECRET_KEY = "mi_clave_secreta"

router = APIRouter(
    prefix="/api/v1/reportes",
    tags=["reportes"]
)


def validar_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except:

        return None


repo = ReporteRepository()

service = ReporteService(repo)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def crear_reporte(
    data: ReporteCreate,
    request: Request,
    db: Session = Depends(get_db)
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
        usuario,
        db
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
                "nombre_usuario": usuario["nombre_completo"],
                "tipo": reporte.tipo,
                "descripcion": reporte.descripcion,
                "evidencias": (
                    reporte.evidencias.split(",")
                    if reporte.evidencias
                    else []
                ),
                "estado": reporte.estado,
                "fecha_reporte": (
                    reporte.fecha_reporte.isoformat()
                )
            }
        }
    )