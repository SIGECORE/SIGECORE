from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional, Dict, Any

# ==================== HU-011: Cancelación de Reserva ====================

class CancelacionResponseData(BaseModel):
    id_reserva: int
    id_zona: int
    nombre_zona: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str
    fecha_cancelacion: datetime

class CancelacionResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[CancelacionResponseData] = None
    error: Optional[Dict[str, Any]] = None