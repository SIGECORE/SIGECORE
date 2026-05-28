# repository/comunicados_repository.py
from typing import Optional
from datetime import datetime

from app.domain.models_domain import (
    Comunicado,
    ComunicadoCreate
)


class ComunicadosRepository:

    def __init__(self):

        self._db: dict[int, Comunicado] = {}
        self._next_id: int = 1

    def create(
        self,
        data: ComunicadoCreate,
        usuario: dict
    ) -> Comunicado:

        comunicado = Comunicado(
            id_comunicado=self._next_id,
            titulo=data.titulo,
            contenido=data.contenido,
            id_autor=usuario["id_usuario"],
            autor_nombre=usuario["nombre_completo"],
            archivos_adjuntos=data.archivos_adjuntos or [],
            fecha_publicacion=datetime.utcnow(),
            fecha_expiracion=data.fecha_expiracion,
            activo=True
        )

        self._db[self._next_id] = comunicado

        self._next_id += 1

        return comunicado