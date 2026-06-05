from datetime import (
    datetime,
    timedelta
)

import bcrypt
import jwt

from fastapi import HTTPException


SECRET_KEY = "mi_clave_secreta"

ALGORITHM = "HS256"


class UsuarioService:

    def __init__(self, repository):

        self.repository = repository

    def create_usuario(
        self,
        data,
        usuario_logueado
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

        usuario = {
            "nombre_completo": data.nombre_completo,
            "email": email,
            "telefono": data.telefono,
            "password_hash": password_hash,
            "id_rol": data.id_rol.value,
            "activo": True,
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
            "ultimo_login": None,
            "fecha_registro": datetime.utcnow()
        }

        usuario = self.repository.create(
            usuario
        )

        usuario["rol_nombre"] = (
            "administrador"
            if usuario["id_rol"] == 1
            else "residente"
        )

        return usuario

    def login(
        self,
        data
    ):

        email = data.email.lower().strip()

        usuario = self.repository.obtener_por_email(
            email
        )

        if not usuario:

            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Credenciales inválidas",
                    "error": {
                        "error_code": "CREDENCIALES_INVALIDAS",
                        "details": "El correo o la contraseña son incorrectos",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        if not usuario["activo"]:

            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Cuenta inactiva",
                    "error": {
                        "error_code": "USUARIO_INACTIVO",
                        "details": "La cuenta está desactivada",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        if (
            usuario["bloqueado_hasta"]
            and usuario["bloqueado_hasta"] > datetime.utcnow()
        ):

            raise HTTPException(
                status_code=423,
                detail={
                    "success": False,
                    "statusCode": 423,
                    "message": "Cuenta bloqueada",
                    "error": {
                        "error_code": "CUENTA_BLOQUEADA",
                        "details": "Demasiados intentos fallidos",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        password_valida = bcrypt.checkpw(
            data.password.encode("utf-8"),
            usuario["password_hash"].encode("utf-8")
        )

        if not password_valida:

            usuario["intentos_fallidos"] += 1

            if usuario["intentos_fallidos"] >= 3:

                usuario["bloqueado_hasta"] = (
                    datetime.utcnow()
                    + timedelta(minutes=30)
                )

            self.repository.actualizar(
                usuario
            )

            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Credenciales inválidas",
                    "error": {
                        "error_code": "CREDENCIALES_INVALIDAS",
                        "details": "El correo o la contraseña son incorrectos",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        usuario["intentos_fallidos"] = 0
        usuario["bloqueado_hasta"] = None
        usuario["ultimo_login"] = datetime.utcnow()

        self.repository.actualizar(
            usuario
        )

        now = datetime.utcnow()

        payload = {
            "id_usuario": usuario["id_usuario"],
            "nombre_completo": usuario["nombre_completo"],
            "email": usuario["email"],
            "id_rol": usuario["id_rol"],
            "iat": now,
            "exp": now + timedelta(hours=8)
        }

        token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {
            "token": token,
            "usuario": {
                "id_usuario": usuario["id_usuario"],
                "nombre_completo": usuario["nombre_completo"],
                "email": usuario["email"],
                "id_rol": usuario["id_rol"],
                "rol_nombre": (
                    "administrador"
                    if usuario["id_rol"] == 1
                    else "residente"
                )
            }
        }

    def actualizar_rol(
        self,
        usuario_id,
        nuevo_rol,
        usuario_logueado,
        ip_origen
    ):

        if usuario_logueado["id_rol"] != 1:

            raise HTTPException(
                status_code=403,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado"
                }
            )

        if usuario_logueado["id_usuario"] == usuario_id:

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "No puedes cambiar tu propio rol"
                }
            )

        usuario = self.repository.obtener_por_id(
            usuario_id
        )

        if not usuario:

            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Usuario no encontrado"
                }
            )

        rol_anterior = usuario["id_rol"]

        usuario["id_rol"] = nuevo_rol

        self.repository.actualizar(
            usuario
        )

        auditoria = {
            "id_usuario_modificado": usuario["id_usuario"],
            "rol_anterior": rol_anterior,
            "rol_nuevo": nuevo_rol,
            "id_usuario_modificador": usuario_logueado["id_usuario"],
            "ip_origen": ip_origen,
            "fecha": datetime.utcnow()
        }

        self.repository.registrar_auditoria(
            auditoria
        )

        return {
            "id_usuario": usuario["id_usuario"],
            "nombre_completo": usuario["nombre_completo"],
            "email": usuario["email"],
            "id_rol": usuario["id_rol"],
            "rol_nombre": (
                "administrador"
                if usuario["id_rol"] == 1
                else "residente"
            ),
            "actualizado_por": (
                f"{usuario_logueado['nombre_completo']} "
                f"(ID: {usuario_logueado['id_usuario']})"
            )
        }