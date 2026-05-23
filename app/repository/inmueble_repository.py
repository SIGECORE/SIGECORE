# repository/inmueble_repository.py
from typing import Optional, List
from domain.models_domain import Inmueble, InmuebleCreate, EstadoInmueble
from datetime import datetime


class InmuebleRepository:

    def __init__(self):
        self._db: dict[int, Inmueble] = {}
        self._next_id: int = 1

    def existe_por_numero_y_torre(self, numero: str, torre: str) -> bool:
        for inmueble in self._db.values():
            if inmueble.numero == numero and inmueble.torre == torre:
                return True
        return False

    def create(self, data: InmuebleCreate) -> Inmueble:
        inmueble = Inmueble(
            id_inmueble=self._next_id,
            numero=data.numero,
            torre=data.torre,
            area_m2=data.area_m2,
            estado=EstadoInmueble.DISPONIBLE,
            fecha_registro=datetime.now(),
            id_propietario=None
        )
        self._db[self._next_id] = inmueble
        self._next_id += 1
        return inmueble