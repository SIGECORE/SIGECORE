from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioToken(BaseModel):
    token: str


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str
    id_rol: int
    rol_nombre: str


class LoginResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: dict


class Usuario(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str
    telefono: str
    password_hash: str
    id_rol: int
    rol_nombre: str
    activo: bool
    fecha_registro: datetime
    intentos_fallidos: int = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None

    class Config:
        from_attributes = True