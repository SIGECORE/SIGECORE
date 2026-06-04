# api/v1/router.py
from fastapi import APIRouter, status, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import jwt

from app.domain.models_domain import Usuario, UsuarioCreate
from app.service.usuario_service import UsuarioService
from app.repository.usuario_repository import UsuarioRepository


SECRET_KEY = "mi_clave_secreta"


def validar_token(token: str) -> dict:
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
    request: Request
):

    # Validar Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "Usuario no autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Token de autenticación requerido",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    # Obtener token
    token = (
        auth_header.split(" ")[1]
        if " " in auth_header
        else auth_header
    )

    usuario = validar_token(token)

    # Validar token
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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

    # Crear usuario
    nuevo_usuario = service.create_usuario(
        data,
        usuario
    )

    # Respuesta exitosa
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
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
                )
            }
        }
    )