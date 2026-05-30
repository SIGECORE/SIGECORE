from datetime import datetime

from fastapi import (
    APIRouter,
    status,
    Request,
    HTTPException,
    Depends
)

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

import jwt

from app.database import get_db

from app.domain.models_domain import (
    UsuarioCreate,
    LoginRequest,
    ActualizarRolRequest
)

from app.service.usuario_service import UsuarioService
from app.repository.usuario_repository import UsuarioRepository


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


repo = UsuarioRepository()

service = UsuarioService(repo)

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["usuarios"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_usuario(
    data: UsuarioCreate,
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
                "message": "Usuario no autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Token requerido",
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
                "message": "Usuario no autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Token inválido o expirado",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    nuevo_usuario = service.create_usuario(
        data,
        usuario,
        db
    )

    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Usuario creado exitosamente",
            "data": {
                "id_usuario": nuevo_usuario.id_usuario,
                "nombre_completo": nuevo_usuario.nombre_completo,
                "email": nuevo_usuario.email,
                "telefono": nuevo_usuario.telefono,
                "id_rol": nuevo_usuario.id_rol,
                "rol_nombre": nuevo_usuario.rol_nombre,
                "activo": nuevo_usuario.activo,
                "fecha_registro": (
                    nuevo_usuario.fecha_registro.isoformat()
                    if nuevo_usuario.fecha_registro
                    else None
                )
            }
        }
    )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
def login_usuario(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    resultado = service.login(
        data,
        db
    )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Inicio de sesión exitoso",
            "data": resultado
        }
    )

@router.patch(
    "/{id}/rol",
    status_code=status.HTTP_200_OK
)
def actualizar_rol(
    id: int,
    data: ActualizarRolRequest,
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

    resultado = service.actualizar_rol(
        id,
        data.id_rol,
        usuario,
        request.client.host,
        db
    )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Rol actualizado exitosamente",
            "data": resultado
        }
    )