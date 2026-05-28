# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EstadoInmueble(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"


# Usuario Schemas
class UsuarioBase(BaseModel):
    nombre_completo: str
    email: str
    telefono: str
    id_rol: int


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    activo: int
    fecha_registro: datetime

    class Config:
        from_attributes = True


# Inmueble Schemas
class InmuebleBase(BaseModel):
    numero: str
    torre: str
    area_m2: float


class InmuebleCreate(InmuebleBase):
    pass


class AsignarPropietarioRequest(BaseModel):
    id_propietario: int


class PropietarioInfo(BaseModel):
    id_propietario: int
    nombre_completo: str
    email: str
    telefono: str


class InmuebleResponse(InmuebleBase):
    id_inmueble: int
    estado: EstadoInmueble
    fecha_registro: datetime
    id_propietario: Optional[int] = None
    propietario: Optional[PropietarioInfo] = None

    class Config:
        from_attributes = True


# Paginación
class PaginacionInfo(BaseModel):
    total: int
    page: int
    limit: int
    total_paginas: int


class ListaInmueblesResponse(BaseModel):
    inmuebles: List[InmuebleResponse]
    paginacion: PaginacionInfo