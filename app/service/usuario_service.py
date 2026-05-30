from datetime import datetime

import bcrypt

from fastapi import HTTPException

from app.models import UsuarioModel


class UsuarioService:

    def __init__(self, repository):
        self.repository = repository

    def create_usuario(
        self,
        data,
        usuario_logueado,
        db
    ):

        if usuario_logueado["id_rol"] != 1:

            raise HTTPException(
                status_code=403,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        email = data.email.lower().strip()

        if self.repository.existe_por_email(
            db,
            email
        ):

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "EMAIL_DUPLICADO",
                        "details": f"El email {email} ya está registrado",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        password_hash = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt(rounds=10)
        ).decode("utf-8")

        usuario = UsuarioModel(
            nombre_completo=data.nombre_completo,
            email=email,
            telefono=data.telefono,
            password_hash=password_hash,
            id_rol=data.id_rol.value,
            activo=True
        )

        usuario = self.repository.create(
            db,
            usuario
        )

        usuario.rol_nombre = (
            "administrador"
            if usuario.id_rol == 1
            else "residente"
        )

        return usuario