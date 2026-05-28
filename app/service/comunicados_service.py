# service/rol_service.py
from fastapi import HTTPException, status
from datetime import datetime

from app.repository.comunicados_repository import (
    ComunicadosRepository
)

from app.domain.models_domain import (
    ComunicadoCreate
)


class ComunicadosService:

    def __init__(
        self,
        repo: ComunicadosRepository
    ):
        self.repo = repo

    def create_comunicado(
        self,
        data: ComunicadoCreate,
        usuario_autenticado: dict
    ):

        # Validar administrador
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
                            "para publicar comunicados"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Validar título
        if not data.titulo:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": (
                            "El campo titulo es obligatorio"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Validar contenido
        if not data.contenido:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": (
                            "El campo contenido es obligatorio"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Validar fecha expiración
        if (
            data.fecha_expiracion
            and data.fecha_expiracion < datetime.utcnow()
        ):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": (
                            "FECHA_EXPIRACION_INVALIDA"
                        ),
                        "details": (
                            "La fecha de expiración no puede "
                            "ser anterior a la fecha actual"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        return self.repo.create(
            data,
            usuario_autenticado
        )