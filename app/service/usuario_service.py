# service/usuario_service.py
from fastapi import HTTPException, status
from datetime import datetime

from app.domain.models_domain import Usuario, UsuarioCreate
from app.repository.usuario_repository import UsuarioRepository


# Constantes de errores
EMAIL_DUPLICADO = "EMAIL_DUPLICADO"
INVALID_DATA = "INVALID_DATA"
ROL_INVALIDO = "ROL_INVALIDO"
ACCESO_DENEGADO = "ACCESO_DENEGADO"


class UsuarioService:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def create_usuario(
        self,
        data: UsuarioCreate,
        usuario_autenticado: dict
    ) -> Usuario:

        # Validar rol administrador
        if usuario_autenticado.get("id_rol") != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": ACCESO_DENEGADO,
                        "details": "Se requiere rol de administrador",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        # Normalizar email
        email_normalizado = data.email.lower()

        # Validar email duplicado
        if self.repo.existe_por_email(email_normalizado):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": EMAIL_DUPLICADO,
                        "details": f"El email {email_normalizado} ya está registrado",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        # Validar longitud de contraseña
        if len(data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": INVALID_DATA,
                        "details": "La contraseña debe tener mínimo 6 caracteres",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        # Validar rol permitido
        if data.id_rol not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": ROL_INVALIDO,
                        "details": "El rol debe ser 1 (administrador) o 2 (residente)",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        # Crear usuario
        return self.repo.create(data)