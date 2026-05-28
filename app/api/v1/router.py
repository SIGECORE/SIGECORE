# api/v1/router.py
from fastapi import (
    APIRouter,
    status,
    Request,
    HTTPException
)

from fastapi.responses import JSONResponse

from datetime import datetime
import jwt
import os

from app.domain.models_domain import (
    ComunicadoCreate
)

from app.repository.comunicados_repository import (
    ComunicadosRepository
)

from app.service.comunicados_service import (
    ComunicadosService
)


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "mi_clave_secreta"
)


def validar_token(token: str) -> dict:

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return {
            "id_usuario": payload.get("id_usuario"),
            "nombre_completo": (
                payload.get("nombre_completo")
            ),
            "email": payload.get("email"),
            "id_rol": payload.get("id_rol")
        }

    except:
        return None


repo = ComunicadosRepository()

service = ComunicadosService(repo)

router = APIRouter(
    prefix="/api/v1/comunicados",
    tags=["comunicados"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_comunicado(
    data: ComunicadoCreate,
    request: Request
):

    auth_header = request.headers.get(
        "Authorization"
    )

    # Validar token
    if not auth_header:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": (
                        "Se requiere un token "
                        "de autenticación válido"
                    ),
                    "timestamp": (
                        datetime.utcnow().isoformat()
                    )
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": (
                        "Token inválido o expirado"
                    ),
                    "timestamp": (
                        datetime.utcnow().isoformat()
                    )
                }
            }
        )

    comunicado = service.create_comunicado(
        data,
        usuario
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "success": True,
            "statusCode": 201,
            "message": (
                "Comunicado publicado exitosamente"
            ),
            "data": {
                "id_comunicado": (
                    comunicado.id_comunicado
                ),
                "titulo": comunicado.titulo,
                "contenido": comunicado.contenido,
                "id_autor": comunicado.id_autor,
                "autor_nombre": (
                    comunicado.autor_nombre
                ),
                "archivos_adjuntos": (
                    comunicado.archivos_adjuntos
                ),
                "fecha_publicacion": (
                    comunicado.fecha_publicacion.isoformat()
                ),
                "fecha_expiracion": (
                    comunicado.fecha_expiracion.isoformat()
                    if comunicado.fecha_expiracion
                    else None
                ),
                "activo": comunicado.activo
            }
        }
    )