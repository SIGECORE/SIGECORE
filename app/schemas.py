from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ZonaComunCreate(BaseModel):
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
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre es obligatorio')
        return v.strip()

class ZonaComunResponse(BaseModel):
    id_zona: int
    nombre: str
    capacidad_maxima: int
    descripcion: Optional[str] = None
    estado: str
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None
    fecha_registro: str