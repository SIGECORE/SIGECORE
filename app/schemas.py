from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional, List, Dict, Any

# ==================== HU-007: Registro de Zonas Comunes ====================

class ZonaCreateRequest(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    capacidad: Optional[int] = None

class ZonaUpdateRequest(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None

class ZonaResponseData(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    capacidad: Optional[int] = None
    estado: str

class ZonaResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[ZonaResponseData] = None
    error: Optional[Dict[str, Any]] = None

class ZonaListResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: Optional[List[ZonaResponseData]] = None
    error: Optional[Dict[str, Any]] = None