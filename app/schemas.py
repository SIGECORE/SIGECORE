from pydantic import BaseModel, Field
from datetime import datetime, time
from typing import Optional, Dict, Any

# ==================== HU-007: Registro de Zonas Comunes ====================

class ZonaCreateRequest(BaseModel):
    nombre: str = Field(..., description="Nombre de la zona común", example="Salón Social")
    capacidad_maxima: int = Field(..., description="Capacidad máxima de personas", example=50)
    descripcion: Optional[str] = Field(None, description="Descripción de la zona", example="Espacio para eventos y reuniones")
    horario_inicio: Optional[time] = Field(None, description="Hora de inicio permitida", example="08:00")
    horario_fin: Optional[time] = Field(None, description="Hora de fin permitida", example="22:00")

class ZonaResponseData(BaseModel):
    id_zona: int
    nombre: str
    capacidad_maxima: int
    descripcion: Optional[str] = None
    estado: str
    horario_inicio: Optional[time] = None
    horario_fin: Optional[time] = None
    fecha_registro: datetime

class ZonaResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[ZonaResponseData] = None
    error: Optional[Dict[str, Any]] = None