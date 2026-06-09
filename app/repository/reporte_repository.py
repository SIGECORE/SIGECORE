# app/repository/reporte_repository.py
from typing import Dict, List, Optional
from domain.models_domain import ReporteResponse, ReporteCreate
from datetime import datetime


class ReporteRepository:

    def __init__(self):
        self._db: Dict[int, ReporteResponse] = {}
        self._next_id: int = 1

    def create(self, data: ReporteCreate, id_usuario: int, nombre_usuario: str) -> ReporteResponse:
        reporte = ReporteResponse(
            id_reporte=self._next_id,
            tipo=data.tipo,
            descripcion=data.descripcion,
            evidencias=data.evidencias,
            id_usuario=id_usuario,
            nombre_usuario=nombre_usuario,
            estado="pendiente",
            fecha_reporte=datetime.now()
        )
        self._db[self._next_id] = reporte
        self._next_id += 1
        return reporte

    def get_by_id(self, reporte_id: int) -> Optional[ReporteResponse]:
        return self._db.get(reporte_id)

    def get_all(self) -> List[ReporteResponse]:
        return list(self._db.values())

    def update_estado(self, reporte_id: int, estado: str, observaciones: str = None, 
                      id_responsable: int = None) -> Optional[ReporteResponse]:
        reporte = self._db.get(reporte_id)
        if not reporte:
            return None
        
        reporte.estado = estado
        if observaciones:
            reporte.observaciones = observaciones
        if id_responsable:
            reporte.id_responsable = id_responsable
        
        if estado == "resuelto":
            reporte.fecha_resolucion = datetime.now()
        
        return reporte