from pydantic import (
    BaseModel,
    field_validator
)

from datetime import datetime
from typing import Optional, List


class ComunicadoCreate(BaseModel):

    titulo: str
    contenido: str
    archivos_adjuntos: List[str] = []
    fecha_expiracion: Optional[datetime] = None

    @field_validator("titulo")
    @classmethod
    def validar_titulo(
        cls,
        value
    ):

        if not value.strip():

            raise ValueError(
                "El campo titulo es obligatorio"
            )

        return value

    @field_validator("contenido")
    @classmethod
    def validar_contenido(
        cls,
        value
    ):

        if not value.strip():

            raise ValueError(
                "El campo contenido es obligatorio"
            )

        return value


class AutorComunicado(BaseModel):

    id_autor: int
    nombre: str


class Comunicado(BaseModel):

    id_comunicado: int
    titulo: str
    contenido: str

    id_autor: int
    autor_nombre: str

    archivos_adjuntos: List[str]

    fecha_publicacion: datetime
    fecha_expiracion: Optional[datetime] = None

    activo: bool

    class Config:
        from_attributes = True