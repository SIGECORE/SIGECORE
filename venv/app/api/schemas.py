from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Esquemas base
class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

# Ejemplo para tu sistema SIGECORE
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: Optional[str] = "usuario"

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Esquemas de respuesta genéricos
class MensajeResponse(BaseModel):
    mensaje: str
    success: bool

class ErrorResponse(BaseModel):
    error: str
    detalle: Optional[str] = None