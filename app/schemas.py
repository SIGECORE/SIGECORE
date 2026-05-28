# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EstadoPago(str, Enum):
    CONFIRMADO = "confirmado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"


# Usuario Schemas
class UsuarioInfo(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str


# Inmueble Schemas
class InmuebleInfo(BaseModel):
    id_inmueble: int
    numero: str
    torre: str


# Pago Schemas
class PagoResponse(BaseModel):
    id_pago: int
    inmueble: InmuebleInfo
    monto: float
    metodo_pago: str
    estado: EstadoPago
    fecha_pago: datetime
    comprobante_url: Optional[str] = None


class HistorialPagosResponse(BaseModel):
    usuario: UsuarioInfo
    pagos: List[PagoResponse]