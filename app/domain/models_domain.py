# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


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