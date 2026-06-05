# app/api/v1/router.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


# ==================== MODELOS ====================

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    password: str


class InmuebleCreate(BaseModel):
    numero: str
    torre: str
    area_m2: float


class ZonaCreate(BaseModel):
    nombre: str
    capacidad_maxima: int
    descripcion: Optional[str] = None
    horario_inicio: Optional[str] = None
    horario_fin: Optional[str] = None


# ==================== ENDPOINTS ====================

@router.post("/usuarios")
def registrar_usuario(data: UsuarioCreate):
    return {"message": f"Usuario {data.nombre} registrado"}


@router.post("/inmuebles")
def crear_inmueble(data: InmuebleCreate):
    return {"message": f"Inmueble {data.numero} creado"}


@router.post("/zonas")
def crear_zona(data: ZonaCreate):
    return {"message": f"Zona {data.nombre} creada"}