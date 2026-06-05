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

    def listar_con_filtros(self, torre: Optional[str] = None, estado: Optional[str] = None,
                           page: int = 1, limit: int = 10) -> tuple[List[InmuebleResponse], int]:
        
        resultados = list(self._db.values())
        
        if torre:
            resultados = [i for i in resultados if i.torre == torre]
        
        if estado:
            resultados = [i for i in resultados if i.estado.value == estado]
        
        resultados.sort(key=lambda x: (x.torre, x.numero))
        
        total = len(resultados)
        start = (page - 1) * limit
        end = start + limit
        
        return resultados[start:end], total