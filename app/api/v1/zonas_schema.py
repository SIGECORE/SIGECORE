from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ZonaComunRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    capacidad_maxima: int
    descripcion: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None

    @validator('capacidad_maxima')
    def validar_capacidad(cls, v):
        if v <= 0:
            raise ValueError('La capacidad máxima debe ser un número entero mayor a 0')
        return v