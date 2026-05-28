from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import Optional, Dict, Any
from enum import Enum

# ==================== Schemas existentes (ajusta según lo que ya tenías) ====================
# Si ya tenías schemas, manténlos y solo agrega los de abajo
# Si no, estos son los básicos que puedes necesitar

class UsuarioBase(BaseModel):
    id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True

class ReservaBase(BaseModel):
    id: int
    zona_id: int
    usuario_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str

    class Config:
        from_attributes = True

# ==================== HU-008: Disponibilidad de Zonas ====================

class DisponibilidadQueryParams(BaseModel):
    zona_id: int = Field(..., description="ID de la zona común")
    fecha: date = Field(..., description="Fecha a consultar (YYYY-MM-DD)")
    hora_inicio: time = Field(..., description="Hora de inicio (HH:MM)")
    hora_fin: time = Field(..., description="Hora de fin (HH:MM)")

class ConflictoInfo(BaseModel):
    id_reserva: int
    usuario: str
    hora_inicio: time
    hora_fin: time

class DisponibilidadData(BaseModel):
    zona_id: int
    nombre: str
    fecha: date
    hora_inicio: time
    hora_fin: time
    disponible: bool
    conflicto_con: Optional[ConflictoInfo] = None

class DisponibilidadResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[DisponibilidadData] = None
    error: Optional[Dict[str, Any]] = None