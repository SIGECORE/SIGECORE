from pydantic import (
    BaseModel,
    field_validator
)

from typing import List


class ReporteCreate(BaseModel):

    tipo: str
    descripcion: str
    evidencias: List[str] = []

    @field_validator("tipo")
    @classmethod
    def validar_tipo(
        cls,
        value
    ):

        tipos_validos = [
            "daño",
            "queja",
            "solicitud"
        ]

        if value not in tipos_validos:

            raise ValueError(
                "El tipo debe ser: daño, queja o solicitud"
            )

        return value

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(
        cls,
        value
    ):

        if not value.strip():

            raise ValueError(
                "El campo descripcion es obligatorio"
            )

        return value