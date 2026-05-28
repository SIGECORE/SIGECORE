# app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Re-exportar desde domain para mantener compatibilidad
from domain.models_domain import (
    InmuebleCartera,
    PropietarioCartera,
    ItemCartera,
    ReporteCarteraResponse
)


# Si quieres tener los modelos también definidos aquí (por si acaso)
class InmuebleCarteraSchema(BaseModel):
    id_inmueble: int
    numero: str
    torre: str
    area_m2: float


class PropietarioCarteraSchema(BaseModel):
    id_propietario: int
    nombre_completo: str
    email: str
    telefono: str


class ItemCarteraSchema(BaseModel):
    inmueble: InmuebleCarteraSchema
    propietario: PropietarioCarteraSchema
    meses_mora: int
    valor_cuota: float
    total_adeudado: float
    ultimo_pago: Optional[str] = None


class ReporteCarteraResponseSchema(BaseModel):
    fecha_generacion: datetime
    total_morosos: int
    total_adeudado: float
    cartera: List[ItemCarteraSchema]