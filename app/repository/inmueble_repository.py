# app/repository/inmueble_repository.py
from typing import Optional, List, Dict
from domain.models_domain import InmuebleResponse, InmuebleCreate, EstadoInmueble
from datetime import datetime


class InmuebleRepository:

    def __init__(self):
        self._db: Dict[int, InmuebleResponse] = {}
        self._next_id: int = 1

    def create(self, data: InmuebleCreate) -> InmuebleResponse:
        inmueble = InmuebleResponse(
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

    def get_by_id(self, inmueble_id: int) -> Optional[InmuebleResponse]:
        return self._db.get(inmueble_id)

    def exists_by_numero_torre(self, numero: str, torre: str) -> bool:
        for inmueble in self._db.values():
            if inmueble.numero == numero and inmueble.torre == torre:
                return True
        return False

    def listar_con_filtros(self, torre=None, estado=None, nombre_propietario=None, page=1, limit=10):
        resultados = list(self._db.values())
        
        if torre:
            resultados = [i for i in resultados if i.torre == torre]
        
        if estado:
            resultados = [i for i in resultados if i.estado.value == estado]
        
        resultados.sort(key=lambda x: (x.torre, x.numero))
        
        total = len(resultados)
        start = (page - 1) * limit
        end = start + limit
        paginados = resultados[start:end]
        
        return paginados, total

    # ==================== HU-005 (Asignación de propietario) ====================
    def asignar_propietario(self, inmueble_id: int, id_propietario: int):
        inmueble = self._db.get(inmueble_id)
        if not inmueble:
            return None
        
        inmueble.id_propietario = id_propietario
        inmueble.estado = EstadoInmueble.OCUPADO
        return inmueble