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

from pydantic import BaseModel
from datetime import datetime


class ComunicadoResponse(BaseModel):

    id_comunicado: int
    titulo: str
    contenido: str
    id_autor: int
    autor_nombre: str
    archivos_adjuntos: list[str]
    fecha_publicacion: datetime
    fecha_expiracion: datetime | None
    activo: bool

class ComunicadoConsultaResponse(BaseModel):

    id_comunicado: int
    titulo: str
    contenido: str
    autor: dict
    archivos_adjuntos: list[str]
    fecha_publicacion: datetime

class ReporteResponse(BaseModel):

    id_reporte: int
    id_usuario: int
    nombre_usuario: str
    tipo: str
    descripcion: str
    evidencias: list[str]
    estado: str
    fecha_reporte: datetime