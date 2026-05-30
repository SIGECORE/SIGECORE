from pydantic import BaseModel
from datetime import datetime


class UsuarioResponse(BaseModel):

    id_usuario: int
    nombre_completo: str
    email: str
    telefono: str
    id_rol: int
    rol_nombre: str
    activo: bool
    fecha_registro: datetime


class LoginResponse(BaseModel):

    token: str
    usuario: dict


class SuccessResponse(BaseModel):

    success: bool
    statusCode: int
    message: str
    data: dict


class ErrorResponse(BaseModel):

    success: bool
    statusCode: int
    message: str
    error: dict