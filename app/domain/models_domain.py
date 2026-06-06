from pydantic import (
    BaseModel,
    EmailStr,
    field_validator
)

from typing import (
    Optional,
    List
)

from datetime import datetime

from enum import Enum


# ==================================================
# USUARIOS
# ==================================================

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


class ActualizarRolRequest(BaseModel):

    id_rol: int

    @field_validator("id_rol")
    @classmethod
    def validar_rol(cls, value):

        if value not in [1, 2]:

            raise ValueError(
                "El rol debe ser 1 (administrador) o 2 (residente)"
            )

        return value


# ==================================================
# COMUNICADOS (HU-013 y HU-014)
# ==================================================

class ComunicadoCreate(BaseModel):

    titulo: str
    contenido: str
    archivos_adjuntos: Optional[List[str]] = []
    fecha_expiracion: Optional[datetime] = None

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, value):

        if not value.strip():

            raise ValueError(
                "El campo titulo es obligatorio"
            )

        return value

    @field_validator("contenido")
    @classmethod
    def validar_contenido(cls, value):

        if not value.strip():

            raise ValueError(
                "El campo contenido es obligatorio"
            )

        return value


class Comunicado(BaseModel):

    id_comunicado: int

    titulo: str

    contenido: str

    id_autor: int

    autor_nombre: str

    archivos_adjuntos: List[str] = []

    fecha_publicacion: datetime

    fecha_expiracion: Optional[datetime] = None

    activo: bool = True

    class Config:
        from_attributes = True


# ==================================================
# REPORTES (HU-018)
# ==================================================

class ReporteCreate(BaseModel):

    tipo: str

    descripcion: str

    evidencias: Optional[List[str]] = []

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, value):

        tipos_validos = [
            "daño",
            "queja",
            "solicitud"
        ]

        if value not in tipos_validos:

            raise ValueError(
                "El tipo debe ser: daño, queja o solicitud"
            )

        return value

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, value):

        if not value.strip():

            raise ValueError(
                "La descripción es obligatoria"
            )

        return value


class Reporte(BaseModel):

    id_reporte: int

    id_usuario: int

    nombre_usuario: str

    tipo: str

    descripcion: str

    evidencias: List[str] = []

    estado: str = "pendiente"

    responsable_id: Optional[int] = None

    observaciones: Optional[str] = None

    fecha_reporte: datetime

    fecha_actualizacion: Optional[datetime] = None

    fecha_resolucion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================================================
# REPORTES (HU-019)
# ==================================================

class ActualizarEstadoReporteRequest(BaseModel):

    estado: str

    observaciones: Optional[str] = None

    id_responsable: Optional[int] = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, value):

        estados_validos = [
            "en_proceso",
            "resuelto"
        ]

        if value not in estados_validos:

            raise ValueError(
                "El estado debe ser: en_proceso o resuelto"
            )

        return value