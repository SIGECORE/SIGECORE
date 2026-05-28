from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional, Dict, Any

# ==================== HU-009: Solicitud de Reserva ====================

class SolicitudReservaRequest(BaseModel):
    id_zona: int = Field(..., description="ID de la zona común a reservar", example=1)
    fecha: date = Field(..., description="Fecha de la reserva (YYYY-MM-DD)", example="2026-05-15")
    hora_inicio: time = Field(..., description="Hora de inicio (HH:MM)", example="14:00")
    hora_fin: time = Field(..., description="Hora de fin (HH:MM)", example="18:00")
    observaciones: Optional[str] = Field(None, description="Observaciones adicionales", example="Cumpleaños familiar")

class ReservaResponseData(BaseModel):
    id_reserva: int
    id_usuario: int
    nombre_usuario: str
    id_zona: int
    nombre_zona: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str
    fecha_solicitud: datetime

class SolicitudReservaResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[ReservaResponseData] = None
    error: Optional[Dict[str, Any]] = None