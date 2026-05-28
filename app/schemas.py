from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional, Dict, Any, List

# ==================== HU-010: Aprobación de Reservas ====================

class SolicitanteInfo(BaseModel):
    id_usuario: int
    nombre: str
    email: str
    telefono: Optional[str] = None

class ZonaInfo(BaseModel):
    id_zona: int
    nombre: str

class ReservaPendienteData(BaseModel):
    id_reserva: int
    solicitante: SolicitanteInfo
    zona: ZonaInfo
    fecha: date
    hora_inicio: time
    hora_fin: time
    observaciones: Optional[str] = None
    fecha_solicitud: datetime

class ReservasPendientesResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[Dict[str, List[ReservaPendienteData]]] = None
    error: Optional[Dict[str, Any]] = None

class CambioEstadoRequest(BaseModel):
    estado: str = Field(..., description="Nuevo estado de la reserva", example="aprobada")

class ReservaEstadoResponseData(BaseModel):
    id_reserva: int
    estado: str
    fecha_aprobacion: Optional[datetime] = None
    aprobado_por: Optional[str] = None

class CambioEstadoResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[ReservaEstadoResponseData] = None
    error: Optional[Dict[str, Any]] = None