# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EstadoInmueble(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"


class PropietarioInfo(BaseModel):
    id_propietario: int
    nombre_completo: str
    email: str
    telefono: str


class Inmueble(BaseModel):
    id_inmueble: int
    numero: str
    torre: str
    area_m2: float
    estado: EstadoInmueble
    fecha_registro: datetime
    id_propietario: Optional[int] = None
    propietario: Optional[PropietarioInfo] = None

    class Config:
        from_attributes = True


class PaginacionInfo(BaseModel):
    total: int
    page: int
    limit: int
    total_paginas: int


class ListaInmueblesResponse(BaseModel):
    inmuebles: List[Inmueble]
    paginacion: PaginacionInfo