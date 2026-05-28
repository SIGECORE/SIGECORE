# domain/models_domain.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Usuario(BaseModel):

    id_usuario: int
    nombre_completo: str
    email: str
    telefono: str
    password_hash: str
    id_rol: int
    rol_nombre: str
    activo: bool = True
    fecha_registro: datetime

    class Config:
        from_attributes = True


class CambiarRolRequest(BaseModel):
    id_rol: int


class AuditoriaRol(BaseModel):

    id_auditoria: int
    id_usuario_modificado: int
    rol_anterior: int
    rol_nuevo: int
    id_usuario_modificador: int
    fecha_modificacion: datetime
    ip_origen: Optional[str] = None