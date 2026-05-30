from pydantic import (
    BaseModel,
    EmailStr,
    field_validator
)

from datetime import datetime
from enum import Enum


class RolUsuario(int, Enum):
    ADMINISTRADOR = 1
    RESIDENTE = 2


class UsuarioBase(BaseModel):

    nombre_completo: str
    email: EmailStr
    telefono: str
    id_rol: RolUsuario

    @field_validator("nombre_completo")
    @classmethod
    def validar_nombre(cls, value):

        if not value.strip():

            raise ValueError(
                "El nombre_completo es obligatorio"
            )

        return value

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, value):

        if not value.strip():

            raise ValueError(
                "El campo telefono es obligatorio"
            )

        if len(value) < 7:

            raise ValueError(
                "El teléfono no es válido"
            )

        return value


class UsuarioCreate(UsuarioBase):

    password: str

    @field_validator("password")
    @classmethod
    def validar_password(cls, value):

        if len(value) < 6:

            raise ValueError(
                "La contraseña debe tener mínimo 6 caracteres"
            )

        return value


class LoginRequest(BaseModel):

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validar_password(cls, value):

        if not value.strip():

            raise ValueError(
                "La contraseña es obligatoria"
            )

        return value


class Usuario(BaseModel):

    id_usuario: int
    nombre_completo: str
    email: str
    telefono: str
    id_rol: int
    rol_nombre: str
    activo: bool
    fecha_registro: datetime

    class Config:
        from_attributes = True
        