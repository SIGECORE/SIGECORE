# app/repository/reserva_repository.py
from typing import Dict, Optional, List
from domain.models_domain import ReservaResponse, ReservaCreate
from datetime import datetime


class ReservaRepository:

    def __init__(self):
        self._db: Dict[int, ReservaResponse] = {}
        self._next_id: int = 1

    def create(self, data: ReservaCreate, id_usuario: int, nombre_usuario: str, nombre_zona: str) -> ReservaResponse:
        reserva = ReservaResponse(
            id_reserva=self._next_id,
            id_usuario=id_usuario,
            nombre_usuario=nombre_usuario,
            id_zona=data.id_zona,
            nombre_zona=nombre_zona,
            fecha=data.fecha,
            hora_inicio=data.hora_inicio,
            hora_fin=data.hora_fin,
            estado="pendiente",
            fecha_solicitud=datetime.now()
        )
        self._db[self._next_id] = reserva
        self._next_id += 1
        return reserva

    def get_by_id(self, reserva_id: int) -> Optional[ReservaResponse]:
        return self._db.get(reserva_id)

    def hay_conflicto(self, zona_id: int, fecha: str, hora_inicio: str, hora_fin: str) -> bool:
        for reserva in self._db.values():
            if reserva.id_zona == zona_id and reserva.fecha == fecha:
                if reserva.estado == "aprobada":
                    if (hora_inicio < reserva.hora_fin and hora_fin > reserva.hora_inicio):
                        return True
        return False