from pydantic import (
    BaseModel,
    field_validator
)

from datetime import datetime


class ComunicadoCreate(BaseModel):

    titulo: str
    contenido: str
    archivos_adjuntos: list[str] = []
    fecha_expiracion: datetime | None = None

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, value):

        if not value.strip():

            raise ValueError(
                "El campo titulo es obligatorio"
            )

        return value

    @field_validator("contenido")
    @classmethod
    def validar_contenido(cls, value):

        if not value.strip():

            raise ValueError(
                "El campo contenido es obligatorio"
            )

        return value