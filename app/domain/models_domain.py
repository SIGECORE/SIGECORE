# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EstadoInmueble(str, Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"


class EstadoPago(str, Enum):
    CONFIRMADO = "confirmado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"


class EstadoZona(str, Enum):
    DISPONIBLE = "disponible"
    MANTENIMIENTO = "mantenimiento"


# ==================== INMUEBLES ====================
class InmuebleBase(BaseModel):
    numero: str
    torre: str
    area_m2: float


class InmuebleCreate(InmuebleBase):
    pass


class InmuebleResponse(InmuebleBase):
    id_inmueble: int
    estado: EstadoInmueble
    fecha_registro: datetime
    id_propietario: Optional[int] = None

    class Config:
        from_attributes = True


class AsignarPropietarioRequest(BaseModel):
    id_propietario: int


class PropietarioInfo(BaseModel):
    id_propietario: int
    nombre_completo: str
    email: str
    telefono: str


class InmuebleConPropietario(InmuebleResponse):
    propietario: Optional[PropietarioInfo] = None


class PaginacionInfo(BaseModel):
    total: int
    page: int
    limit: int
    total_paginas: int


class ListaInmueblesResponse(BaseModel):
    inmuebles: List[InmuebleConPropietario]
    paginacion: PaginacionInfo


# ==================== PAGOS ====================
class PagoRequest(BaseModel):
    id_inmueble: int
    monto: float
    metodo_pago: str
    token_pasarela: str


class PagoResponse(BaseModel):
    id_pago: int
    id_usuario: int
    id_inmueble: int
    monto: float
    metodo_pago: str
    estado: EstadoPago
    fecha_pago: datetime
    comprobante_url: Optional[str] = None

    class Config:
        from_attributes = True


class UsuarioInfo(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str


class InmuebleInfo(BaseModel):
    id_inmueble: int
    numero: str
    torre: str


class PagoHistorialResponse(BaseModel):
    id_pago: int
    inmueble: InmuebleInfo
    monto: float
    metodo_pago: str
    estado: EstadoPago
    fecha_pago: datetime
    comprobante_url: Optional[str] = None


class HistorialPagosResponse(BaseModel):
    usuario: UsuarioInfo
    pagos: List[PagoHistorialResponse]


class InmuebleCartera(BaseModel):
    id_inmueble: int
    numero: str
    torre: str
    area_m2: float


class PropietarioCartera(BaseModel):
    id_propietario: int
    nombre_completo: str
    email: str
    telefono: str


class ItemCartera(BaseModel):
    inmueble: InmuebleCartera
    propietario: PropietarioCartera
    meses_mora: int
    valor_cuota: float
    total_adeudado: float
    ultimo_pago: Optional[str] = None


class ReporteCarteraResponse(BaseModel):
    fecha_generacion: datetime
    total_morosos: int
    total_adeudado: float
    cartera: List[ItemCartera]


# ==================== ZONAS COMUNES ====================
class ZonaBase(BaseModel):
    nombre: str
    capacidad_maxima: int
    descripcion: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None


class ZonaCreate(ZonaBase):
    pass


class ZonaResponse(ZonaBase):
    id_zona: int
    estado: EstadoZona
    fecha_registro: datetime

    class Config:
        from_attributes = True


class ZonaInfo(BaseModel):
    zona_id: int
    nombre: str


class ConflictoInfo(BaseModel):
    id_reserva: int
    usuario: str
    hora_inicio: str
    hora_fin: str


class DisponibilidadData(BaseModel):
    zona_id: int
    nombre: str
    fecha: str
    hora_inicio: str
    hora_fin: str
    disponible: bool
    conflicto_con: Optional[ConflictoInfo] = None


class DisponibilidadResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: DisponibilidadData


# ==================== USUARIOS (HU-001 y HU-002) ====================
class UsuarioCreate(BaseModel):
    nombre_completo: str
    email: str
    telefono: str
    password: str
    id_rol: int


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str
    telefono: str
    id_rol: int
    activo: int
    fecha_registro: datetime
    intentos_fallidos: Optional[int] = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str


class UsuarioLoginResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str
    id_rol: int
    rol_nombre: str


class LoginResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: dict


# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ==================== HU-002 (Inicio de sesión) ====================

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: dict


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre_completo: str
    email: str
    telefono: str
    id_rol: int
    activo: int
    fecha_registro: datetime
    intentos_fallidos: Optional[int] = 0
    bloqueado_hasta: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None
