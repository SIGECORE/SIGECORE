# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoInmueble(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"


class EstadoPago(str, Enum):
    CONFIRMADO = "confirmado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"


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


class PagoRequest(BaseModel):
    id_inmueble: int
    monto: float
    metodo_pago: str
    token_pasarela: str


class PagoResponse(BaseModel):
    id_pago: int
    id_usuario: int
    id_inmueble: int
    monto: float
    metodo_pago: str
    estado: EstadoPago
    fecha_pago: datetime
    comprobante_url: str

    class Config:
        from_attributes = True