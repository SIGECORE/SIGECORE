# app/repository/inmueble_repository.py
from typing import Optional, Dict
from domain.models_domain import Inmueble


class InmuebleRepository:
    
    def __init__(self):
        self._db: Dict[int, Inmueble] = {}

    def agregar_inmueble(self, inmueble: Inmueble):
        self._db[inmueble.id_inmueble] = inmueble

    def get_by_id(self, inmueble_id: int) -> Optional[Inmueble]:
        return self._db.get(inmueble_id)