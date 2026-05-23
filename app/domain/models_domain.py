from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional

class ZonaComunDomain(BaseModel):
    id_zona: Optional[int] = None
    nombre: str
    capacidad_maxima: int
    descripcion: Optional[str] = None
    estado: str = "disponible"
    horario_inicio: Optional[time] = None
    horario_fin: Optional[time] = None
    fecha_registro: Optional[datetime] = None