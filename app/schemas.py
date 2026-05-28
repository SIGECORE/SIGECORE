from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional, Dict, Any, List

# ==================== HU-012: Consulta de Reservas por Usuario ====================

class UsuarioInfo(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: Optional[str] = None

class ZonaReservaInfo(BaseModel):
    id_zona: int
    nombre: str

class ReservaHistorialItem(BaseModel):
    id_reserva: int
    zona: ZonaReservaInfo
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str
    fecha_solicitud: datetime

class ConsultaReservasData(BaseModel):
    usuario: UsuarioInfo
    reservas: List[ReservaHistorialItem]

class ConsultaReservasResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[ConsultaReservasData] = None
    error: Optional[Dict[str, Any]] = None