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
    CambiarRolRequest
)

from app.repository.rol_repository import (
    RolRepository
)

from app.service.rol_service import (
    RolService
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "mi_clave_secreta"
)

ALGORITHM = "HS256"


def validar_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return {
            "id_usuario": payload.get(
                "id_usuario"
            ),
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

    except:

        return None


repo = RolRepository()
service = RolService(repo)

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["roles"]
)


@router.patch("/{id_usuario}/rol")
def cambiar_rol(
    id_usuario: int,
    data: CambiarRolRequest,
    request: Request
):

    auth_header = request.headers.get(
        "Authorization"
    )

    # No autenticado
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

    usuario_actualizado = service.cambiar_rol(
        id_usuario=id_usuario,
        data=data,
        usuario_autenticado=usuario,
        ip_origen=request.client.host
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "statusCode": 200,
            "message": (
                "Rol actualizado exitosamente"
            ),
            "data": {
                "id_usuario": (
                    usuario_actualizado.id_usuario
                ),
                "nombre_completo": (
                    usuario_actualizado.nombre_completo
                ),
                "email": (
                    usuario_actualizado.email
                ),
                "id_rol": (
                    usuario_actualizado.id_rol
                ),
                "rol_nombre": (
                    usuario_actualizado.rol_nombre
                ),
                "actualizado_por": (
                    f"{usuario['nombre_completo']} "
                    f"(ID: {usuario['id_usuario']})"
                )
            }
        }
    )