# app/repository/inmueble_repository.py
from typing import Optional, List, Dict
from domain.models_domain import Inmueble, InmuebleCreate, EstadoInmueble, PropietarioInfo
from datetime import datetime


class InmuebleRepository:

    def __init__(self):
        self._db: dict[int, Inmueble] = {}
        self._next_id: int = 1
        self._auditoria: List[Dict] = []

    def get_by_id(self, inmueble_id: int) -> Optional[Inmueble]:
        return self._db.get(inmueble_id)

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

    def asignar_propietario(self, inmueble_id: int, id_propietario: int, id_administrador: int, propietario_data: dict) -> Optional[Inmueble]:
        inmueble = self._db.get(inmueble_id)
        if not inmueble:
            return None
        
        propietario_anterior = inmueble.id_propietario
        
        inmueble.id_propietario = id_propietario
        inmueble.estado = EstadoInmueble.OCUPADO
        inmueble.propietario = PropietarioInfo(**propietario_data)
        
        self._auditoria.append({
            "id_inmueble": inmueble_id,
            "id_propietario_anterior": propietario_anterior,
            "id_propietario_nuevo": id_propietario,
            "id_usuario_modificador": id_administrador,
            "fecha_modificacion": datetime.now()
        })
        
        return inmueble