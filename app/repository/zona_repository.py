# app/repository/zona_repository.py
from typing import Optional, Dict, List
from domain.models_domain import ZonaResponse, ZonaCreate, EstadoZona
from datetime import datetime


class ZonaRepository:

    def __init__(self):
        self._db: Dict[int, ZonaResponse] = {}
        self._next_id: int = 1

    def get_by_id(self, zona_id: int) -> Optional[ZonaResponse]:
        return self._db.get(zona_id)

    def exists_by_nombre(self, nombre: str) -> bool:
        for zona in self._db.values():
            if zona.nombre.lower() == nombre.lower():
                return True
        return False

    def create(self, data: ZonaCreate) -> ZonaResponse:
        zona = ZonaResponse(
            id_zona=self._next_id,
            nombre=data.nombre,
            capacidad_maxima=data.capacidad_maxima,
            descripcion=data.descripcion,
            horario_inicio=data.horario_inicio,
            horario_fin=data.horario_fin,
            estado=EstadoZona.DISPONIBLE,
            fecha_registro=datetime.now()
        )
        self._db[self._next_id] = zona
        self._next_id += 1
        return zona

    def get_all(self) -> List[ZonaResponse]:
        return list(self._db.values())