# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class InmuebleCartera(BaseModel):
    id_inmueble: int
    numero: str
    torre: str
    area_m2: float


class PropietarioCartera(BaseModel):
    id_propietario: int
    nombre_completo: str
    email: str
    telefono: str


class ItemCartera(BaseModel):
    inmueble: InmuebleCartera
    propietario: PropietarioCartera
    meses_mora: int
    valor_cuota: float
    total_adeudado: float
    ultimo_pago: Optional[str] = None


class ReporteCarteraResponse(BaseModel):
    fecha_generacion: datetime
    total_morosos: int
    total_adeudado: float
    cartera: List[ItemCartera]