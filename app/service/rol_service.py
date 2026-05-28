# service/rol_service.py
from fastapi import HTTPException, status
from datetime import datetime

from app.repository.rol_repository import RolRepository
from app.domain.models_domain import (
    CambiarRolRequest
)


class RolService:

    def __init__(
        self,
        repo: RolRepository
    ):

        self.repo = repo

    def cambiar_rol(
        self,
        id_usuario: int,
        data: CambiarRolRequest,
        usuario_autenticado: dict,
        ip_origen: str | None = None
    ):

        # Validar admin
        if usuario_autenticado.get("id_rol") != 1:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": (
                            "Se requiere rol de administrador "
                            "para realizar esta acción"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Validar auto modificación
        if (
            usuario_autenticado.get("id_usuario")
            == id_usuario
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": (
                            "AUTO_MODIFICACION_NO_PERMITIDA"
                        ),
                        "details": (
                            "No puedes cambiar tu propio rol "
                            "de administrador"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Validar rol
        if data.id_rol not in [1, 2]:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "ROL_INVALIDO",
                        "details": (
                            "El rol debe ser 1 "
                            "(administrador) "
                            "o 2 (residente)"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        usuario = self.repo.buscar_usuario_por_id(
            id_usuario
        )

        # Usuario no encontrado
        if not usuario:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Usuario no encontrado",
                    "error": {
                        "error_code": "USUARIO_NOT_FOUND",
                        "details": (
                            f"No existe un usuario "
                            f"con el ID {id_usuario}"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        rol_anterior = usuario.id_rol

        usuario_actualizado = self.repo.actualizar_rol(
            usuario,
            data.id_rol
        )

        # Auditoría
        self.repo.registrar_auditoria(
            id_usuario_modificado=id_usuario,
            rol_anterior=rol_anterior,
            rol_nuevo=data.id_rol,
            id_usuario_modificador=(
                usuario_autenticado.get("id_usuario")
            ),
            ip_origen=ip_origen
        )

        return usuario_actualizado