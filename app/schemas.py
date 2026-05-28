# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoPago(str, Enum):
    CONFIRMADO = "confirmado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"


# Pago Schemas
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
    comprobante_url: Optional[str] = None

    class Config:
        from_attributes = True
        