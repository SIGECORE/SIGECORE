from pydantic import BaseModel
from typing import Optional, List
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


class InmuebleResponse(InmuebleBase):
    id_inmueble: int
    estado: EstadoInmueble
    fecha_registro: datetime
    id_propietario: Optional[int] = None

    class Config:
        from_attributes = True


class PropietarioInfo(BaseModel):
    id_propietario: int
    nombre_completo: str
    email: str
    telefono: str


class InmuebleConPropietario(InmuebleResponse):
    propietario: Optional[PropietarioInfo] = None


class PaginacionInfo(BaseModel):
    total: int
    page: int
    limit: int
    total_paginas: int


class ListaInmueblesResponse(BaseModel):
    inmuebles: List[InmuebleConPropietario]
    paginacion: PaginacionInfo