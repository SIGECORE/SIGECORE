from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Usuario(BaseModel):

    id_usuario: int
    nombre_completo: str
    email: str
    telefono: Optional[str] = None
    id_rol: int
    rol_nombre: str
    activo: bool
    password_hash: str
    intentos_fallidos: int = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None


class UsuarioCreate(BaseModel):

    nombre_completo: str
    email: str
    telefono: str
    password: str
    id_rol: int


# ===== DEPENDENCIA HISTORIA 1 =====
# Este modelo viene de HU-001
# porque login necesita usuarios registrados

class UsuarioLogin(BaseModel):

    email: str
    password: str