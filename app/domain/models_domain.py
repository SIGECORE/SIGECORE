# domain/models_domain.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ComunicadoCreate(BaseModel):
    titulo: str
    contenido: str
    archivos_adjuntos: Optional[List[str]] = []
    fecha_expiracion: Optional[datetime] = None


class Comunicado(BaseModel):
    id_comunicado: int
    titulo: str
    contenido: str
    id_autor: int
    autor_nombre: str
    archivos_adjuntos: List[str]
    fecha_publicacion: datetime
    fecha_expiracion: Optional[datetime]
    activo: bool