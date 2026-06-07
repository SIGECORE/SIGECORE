# app/service/auth_service.py
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status
from domain.models_domain import LoginRequest, LoginResponse
from repository.usuario_repository import UsuarioRepository


SECRET_KEY = "mi_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class AuthService:

    def __init__(self, usuario_repo: UsuarioRepository):
        self.usuario_repo = usuario_repo
        # Crear usuario de prueba si no existe
        if not self.usuario_repo.get_by_email("juan@example.com"):
            self.usuario_repo.create_default_user()

    def login(self, login_data: LoginRequest) -> LoginResponse:
        
        # Validar campos obligatorios
        if not login_data.email or not login_data.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "Los campos email y password son obligatorios",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Buscar usuario por email
        usuario = self.usuario_repo.get_by_email(login_data.email)
        
        # Si no existe, mensaje genérico
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Credenciales inválidas",
                    "error": {
                        "error_code": "CREDENCIALES_INVALIDAS",
                        "details": "El correo o la contraseña son incorrectos",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Verificar si la cuenta está bloqueada
        if usuario.bloqueado_hasta and usuario.bloqueado_hasta > datetime.now():
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail={
                    "success": False,
                    "statusCode": 423,
                    "message": "Cuenta bloqueada",
                    "error": {
                        "error_code": "CUENTA_BLOQUEADA",
                        "details": "Demasiados intentos fallidos. Cuenta bloqueada por 30 minutos.",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Verificar si el usuario está activo
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "Cuenta inactiva",
                    "error": {
                        "error_code": "USUARIO_INACTIVO",
                        "details": "La cuenta del usuario está desactivada. Contacte al administrador.",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Verificar contraseña (simulada)
        password_valida = (login_data.password == "123456")
        
        if not password_valida:
            nuevos_intentos = (usuario.intentos_fallidos or 0) + 1
            if nuevos_intentos >= 3:
                bloqueado_hasta = datetime.now() + timedelta(minutes=30)
                self.usuario_repo.update_intentos(usuario.id_usuario, nuevos_intentos, bloqueado_hasta)
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail={
                        "success": False,
                        "statusCode": 423,
                        "message": "Cuenta bloqueada",
                        "error": {
                            "error_code": "CUENTA_BLOQUEADA",
                            "details": "Demasiados intentos fallidos. Cuenta bloqueada por 30 minutos.",
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                )
            else:
                self.usuario_repo.update_intentos(usuario.id_usuario, nuevos_intentos)
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "success": False,
                        "statusCode": 401,
                        "message": "Credenciales inválidas",
                        "error": {
                            "error_code": "CREDENCIALES_INVALIDAS",
                            "details": "El correo o la contraseña son incorrectos",
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                )
        
        # Login exitoso
        self.usuario_repo.reset_intentos(usuario.id_usuario)
        self.usuario_repo.update_ultimo_login(usuario.id_usuario)
        
        token_data = {
            "id_usuario": usuario.id_usuario,
            "nombre_completo": usuario.nombre_completo,
            "email": usuario.email,
            "id_rol": usuario.id_rol
        }
        token = create_access_token(token_data)
        
        rol_nombre = "administrador" if usuario.id_rol == 1 else "residente"
        
        return LoginResponse(
            success=True,
            statusCode=200,
            message="Inicio de sesión exitoso",
            data={
                "token": token,
                "usuario": {
                    "id_usuario": usuario.id_usuario,
                    "nombre_completo": usuario.nombre_completo,
                    "email": usuario.email,
                    "id_rol": usuario.id_rol,
                    "rol_nombre": rol_nombre
                }
            }
        )