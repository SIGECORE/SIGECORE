# app/domain/models_domain.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ==================== HU-001 (Usuario base) ====================

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


# ==================== HU-002 (Inicio de sesión) ====================

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    data: dict


# ==================== HU-003 (Asignación de roles) ====================

class AsignarRolRequest(BaseModel):
    id_rol: int


class AuditoriaRolResponse(BaseModel):
    id_auditoria: int
    id_usuario_modificado: int
    rol_anterior: int
    rol_nuevo: int
    id_usuario_modificador: int
    fecha_modificacion: datetime
    ip_origen: Optional[str] = None


# ==================== HU-004 (Registro de inmuebles) ====================

class InmuebleBase(BaseModel):
    numero: str
    torre: str
    area_m2: float


class InmuebleCreate(InmuebleBase):
    pass


class InmuebleResponse(InmuebleBase):
    id_inmueble: int
    estado: str
    fecha_registro: datetime
    id_propietario: Optional[int] = None


# ==================== HU-005 (Asignación de propietario) ====================

class AsignarPropietarioRequest(BaseModel):
    id_propietario: int


# ==================== HU-006 (Consulta de inmuebles) ====================

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


# ==================== HU-007 (Registro de zonas comunes) ====================

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
    estado: str
    fecha_registro: datetime


# ==================== HU-008 (Consulta disponibilidad zonas) ====================

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


# ==================== HU-015 (Registro de pago) ====================

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
    estado: str
    fecha_pago: datetime
    comprobante_url: Optional[str] = None


# ==================== HU-016 (Historial de pagos) ====================

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
    estado: str
    fecha_pago: datetime
    comprobante_url: Optional[str] = None


class HistorialPagosResponse(BaseModel):
    usuario: UsuarioInfo
    pagos: List[PagoHistorialResponse]


# ==================== HU-017 (Reporte de cartera) ====================

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