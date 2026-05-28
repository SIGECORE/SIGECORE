# service/usuario_service.py
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

from app.repository.usuario_repository import UsuarioRepository
from app.domain.models_domain import UsuarioLogin


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "mi_clave_secreta"
)

ALGORITHM = "HS256"


class UsuarioService:

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def login(
        self,
        data: UsuarioLogin
    ):

        email = data.email.lower()

        usuario = self.repo.buscar_por_email(email)

        # Usuario no existe
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Credenciales inválidas",
                    "error": {
                        "error_code": "CREDENCIALES_INVALIDAS",
                        "details": (
                            "El correo o la contraseña son incorrectos"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Usuario inactivo
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Cuenta inactiva",
                    "error": {
                        "error_code": "USUARIO_INACTIVO",
                        "details": (
                            "La cuenta del usuario está desactivada"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Cuenta bloqueada
        if (
            usuario.bloqueado_hasta
            and usuario.bloqueado_hasta > datetime.utcnow()
        ):
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail={
                    "success": False,
                    "statusCode": 423,
                    "message": "Cuenta bloqueada",
                    "error": {
                        "error_code": "CUENTA_BLOQUEADA",
                        "details": (
                            "Demasiados intentos fallidos"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Verificar password
        password_correcto = bcrypt.checkpw(
            data.password.encode("utf-8"),
            usuario.password_hash.encode("utf-8")
        )

        if not password_correcto:

            nuevos_intentos = (
                usuario.intentos_fallidos + 1
            )

            self.repo.actualizar_intentos(
                usuario,
                nuevos_intentos
            )

            # Bloquear después de 3 intentos
            if nuevos_intentos >= 3:

                bloqueo = (
                    datetime.utcnow() + timedelta(minutes=30)
                )

                self.repo.bloquear_usuario(
                    usuario,
                    bloqueo
                )

                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail={
                        "success": False,
                        "statusCode": 423,
                        "message": "Cuenta bloqueada",
                        "error": {
                            "error_code": "CUENTA_BLOQUEADA",
                            "details": (
                                "Cuenta bloqueada por 30 minutos"
                            ),
                            "timestamp": (
                                datetime.utcnow().isoformat()
                            )
                        }
                    }
                )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Credenciales inválidas",
                    "error": {
                        "error_code": "CREDENCIALES_INVALIDAS",
                        "details": (
                            "El correo o la contraseña son incorrectos"
                        ),
                        "timestamp": (
                            datetime.utcnow().isoformat()
                        )
                    }
                }
            )

        # Resetear intentos
        self.repo.resetear_intentos(usuario)

        # Actualizar último login
        self.repo.actualizar_ultimo_login(usuario)

        # JWT
        fecha_actual = datetime.utcnow()

        payload = {
            "id_usuario": usuario.id_usuario,
            "nombre_completo": usuario.nombre_completo,
            "email": usuario.email,
            "id_rol": usuario.id_rol,
            "iat": fecha_actual,
            "exp": fecha_actual + timedelta(hours=8)
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "token": token,
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "nombre_completo": usuario.nombre_completo,
                "email": usuario.email,
                "id_rol": usuario.id_rol,
                "rol_nombre": usuario.rol_nombre
            }
        }