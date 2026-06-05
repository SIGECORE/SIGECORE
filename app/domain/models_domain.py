# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoInmueble(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"


class InmuebleBase(BaseModel):
    numero: str
    torre: str
    area_m2: float


class InmuebleCreate(InmuebleBase):
    pass


class Inmueble(InmuebleBase):
    id_inmueble: int
    estado: EstadoInmueble
    fecha_registro: datetime
    id_propietario: Optional[int] = None

    class Config:
        from_attributes = True
        
class EstadoZona(str, Enum):
    DISPONIBLE = "disponible"
    MANTENIMIENTO = "mantenimiento"


class ZonaBase(BaseModel):
    nombre: str
    capacidad_maxima: int
    descripcion: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None


class ZonaCreate(ZonaBase):
    pass


class ZonaResponse(ZonaBase):
    id_zona: int
    estado: EstadoZona
    fecha_registro: datetime

    class Config:
        from_attributes = True        