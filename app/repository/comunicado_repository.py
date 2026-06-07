# app/repository/comunicado_repository.py
from typing import Dict, List, Optional
from domain.models_domain import ComunicadoResponse, ComunicadoCreate
from datetime import datetime


class ComunicadoRepository:

    def __init__(self):
        self._db: Dict[int, ComunicadoResponse] = {}
        self._next_id: int = 1

    def create(self, data: ComunicadoCreate, id_autor: int, autor_nombre: str) -> ComunicadoResponse:
        comunicado = ComunicadoResponse(
            id_comunicado=self._next_id,
            titulo=data.titulo,
            contenido=data.contenido,
            archivos_adjuntos=data.archivos_adjuntos,
            fecha_expiracion=data.fecha_expiracion,
            id_autor=id_autor,
            autor_nombre=autor_nombre,
            fecha_publicacion=datetime.now(),
            activo=True
        )
        self._db[self._next_id] = comunicado
        self._next_id += 1
        return comunicado

    def get_activos(self) -> List[ComunicadoResponse]:
        ahora = datetime.now()
        activos = []
        for comunicado in self._db.values():
            if comunicado.activo:
                if comunicado.fecha_expiracion is None or comunicado.fecha_expiracion > ahora:
                    activos.append(comunicado)
        activos.sort(key=lambda x: x.fecha_publicacion, reverse=True)
        return activos

    def get_by_id(self, comunicado_id: int) -> Optional[ComunicadoResponse]:
        return self._db.get(comunicado_id)

    def desactivar(self, comunicado_id: int) -> bool:
        comunicado = self._db.get(comunicado_id)
        if comunicado:
            comunicado.activo = False
            return True
        return False