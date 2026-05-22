# domain/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


# ── Enums ──
class EstadoInmueble(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"


# ── Modelo base: campos comunes ──
class InmuebleBase(BaseModel):
    numero: str
    torre: str
    area_m2: float


# ── Para CREAR un inmueble (sin ID) ──
class InmuebleCreate(InmuebleBase):
    pass


# ── Respuesta completa (con ID) ──
class Inmueble(InmuebleBase):
    id_inmueble: int
    estado: EstadoInmueble
    fecha_registro: datetime
    id_propietario: Optional[int] = None

    class Config:
        from_attributes = True