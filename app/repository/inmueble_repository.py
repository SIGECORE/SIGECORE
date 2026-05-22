# repository/inmueble_repository.py
from typing import Optional, List
from domain.models_domain import Inmueble, InmuebleCreate, EstadoInmueble
from datetime import datetime


class InmuebleRepository:
    """Simulamos una base de datos con un dict."""

    def __init__(self):
        self._db: dict[int, Inmueble] = {}
        self._next_id: int = 1

    def get_all(self) -> List[Inmueble]:
        return list(self._db.values())

    def get_by_id(self, inmueble_id: int) -> Optional[Inmueble]:
        return self._db.get(inmueble_id)

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

    def delete(self, inmueble_id: int) -> bool:
        if inmueble_id in self._db:
            del self._db[inmueble_id]
            return True
        return False