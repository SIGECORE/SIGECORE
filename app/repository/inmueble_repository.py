# app/repository/inmueble_repository.py
from typing import Optional, List, Dict
from domain.models_domain import Inmueble, EstadoInmueble, PropietarioInfo
from datetime import datetime


class InmuebleRepository:

    def __init__(self):
        self._db: dict[int, Inmueble] = {}
        self._next_id: int = 1

    def crear_inmueble(self, numero: str, torre: str, area_m2: float) -> Inmueble:
        inmueble = Inmueble(
            id_inmueble=self._next_id,
            numero=numero,
            torre=torre,
            area_m2=area_m2,
            estado=EstadoInmueble.DISPONIBLE,
            fecha_registro=datetime.now(),
            id_propietario=None
        )
        self._db[self._next_id] = inmueble
        self._next_id += 1
        return inmueble

    def get_all(self) -> List[Inmueble]:
        return list(self._db.values())

    def get_by_id(self, inmueble_id: int) -> Optional[Inmueble]:
        return self._db.get(inmueble_id)

    def asignar_propietario(self, inmueble_id: int, id_propietario: int, propietario_data: dict) -> Optional[Inmueble]:
        inmueble = self._db.get(inmueble_id)
        if not inmueble:
            return None
        inmueble.id_propietario = id_propietario
        inmueble.estado = EstadoInmueble.OCUPADO
        inmueble.propietario = PropietarioInfo(**propietario_data)
        return inmueble

    def listar_con_filtros(self, torre: Optional[str] = None, estado: Optional[str] = None, 
                           nombre_propietario: Optional[str] = None, page: int = 1, limit: int = 10) -> tuple[List[Inmueble], int]:
        
        resultados = list(self._db.values())
        
        # Aplicar filtros
        if torre:
            resultados = [i for i in resultados if i.torre.lower() == torre.lower()]
        
        if estado:
            resultados = [i for i in resultados if i.estado.value == estado]
        
        if nombre_propietario:
            resultados = [i for i in resultados if i.propietario and nombre_propietario.lower() in i.propietario.nombre_completo.lower()]
        
        # Ordenar por torre y numero
        resultados.sort(key=lambda x: (x.torre, x.numero))
        
        total = len(resultados)
        
        # Paginación
        start = (page - 1) * limit
        end = start + limit
        paginados = resultados[start:end]
        
        return paginados, total