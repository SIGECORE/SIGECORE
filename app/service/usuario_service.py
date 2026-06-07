<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
from datetime import (
    datetime,
    timedelta
)
<<<<<<< HEAD
=======
<<<<<<< HEAD

import bcrypt
import jwt

from fastapi import HTTPException


SECRET_KEY = "mi_clave_secreta"
=======
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae

import bcrypt
import jwt

from fastapi import HTTPException


SECRET_KEY = "mi_clave_secreta"

ALGORITHM = "HS256"
<<<<<<< HEAD
=======
=======
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
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae


class UsuarioService:

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
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
<<<<<<< HEAD
=======
=======
=======
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6

    def create_usuario(
        self,
        data: UsuarioCreate,
        usuario_autenticado: dict
    ) -> Usuario:

        # Validar rol administrador
        if usuario_autenticado.get("id_rol") != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
<<<<<<< HEAD
                        "error_code": "ACCESO_DENEGADO",
=======
                        "error_code": ACCESO_DENEGADO,
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
                        "details": "Se requiere rol de administrador",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

<<<<<<< HEAD
        email = data.email.lower().strip()

        if self.repository.existe_por_email(email):

            raise HTTPException(
                status_code=400,
=======
        # Normalizar email
        email_normalizado = data.email.lower()

        # Validar email duplicado
        if self.repo.existe_por_email(email_normalizado):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
<<<<<<< HEAD
                        "error_code": "EMAIL_DUPLICADO",
                        "details": f"El email {email} ya está registrado",
=======
                        "error_code": EMAIL_DUPLICADO,
                        "details": f"El email {email_normalizado} ya está registrado",
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

<<<<<<< HEAD
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

        usuario = self.repository.create(usuario)

        usuario["rol_nombre"] = (
            "administrador"
            if usuario["id_rol"] == 1
            else "residente"
        )

        return usuario
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae

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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
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
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
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
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
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
<<<<<<< HEAD
                        "details": "Demasiados intentos fallidos",
=======
<<<<<<< HEAD
                        "details": "Demasiados intentos fallidos",
=======
                        "details": "Cuenta bloqueada por demasiados intentos",
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae

            if usuario["intentos_fallidos"] >= 3:

                usuario["bloqueado_hasta"] = (
                    datetime.utcnow()
                    + timedelta(minutes=30)
                )

            self.repository.actualizar(
                usuario
            )

<<<<<<< HEAD
=======
=======

            if usuario["intentos_fallidos"] >= 3:

                usuario["bloqueado_hasta"] = (
                    datetime.utcnow()
                    + timedelta(minutes=30)
                )

            self.repository.actualizar(usuario)

>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
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

<<<<<<< HEAD
        self.repository.actualizar(
            usuario
        )
=======
<<<<<<< HEAD
        self.repository.actualizar(
            usuario
        )
=======
        self.repository.actualizar(usuario)
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae

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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae

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
<<<<<<< HEAD
        }
=======
        }
=======
=======
        # Crear usuario
        return self.repo.create(data)
>>>>>>> 62197992c9e421bb975a958381525013c2d14f56
>>>>>>> e610f025d06aa9c255563bd80874e3d412c1aba6
>>>>>>> 76ac4f2b480b2cf48108dd35ad15c738644454ae
