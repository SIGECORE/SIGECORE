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