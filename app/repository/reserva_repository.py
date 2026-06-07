# app/repository/reserva_repository.py
from typing import Dict, Optional, List


class ReservaRepository:

    def __init__(self):
        self._db: Dict[int, dict] = {}
        self._next_id: int = 1

    def agregar_reserva(self, reserva: dict) -> dict:
        reserva["id_reserva"] = self._next_id
        self._db[self._next_id] = reserva
        self._next_id += 1
        return reserva

    def get_reservas_by_zona_y_fecha(self, zona_id: int, fecha: str) -> List[dict]:
        reservas = []
        for reserva in self._db.values():
            if reserva.get("zona_id") == zona_id and reserva.get("fecha") == fecha:
                if reserva.get("estado") == "aprobada":
                    reservas.append(reserva)
        return reservas

    def hay_conflicto(self, zona_id: int, fecha: str, hora_inicio: str, hora_fin: str) -> Optional[dict]:
        for reserva in self._db.values():
            if reserva.get("zona_id") == zona_id and reserva.get("fecha") == fecha:
                if reserva.get("estado") == "aprobada":
                    reserva_inicio = reserva.get("hora_inicio")
                    reserva_fin = reserva.get("hora_fin")
                    if (hora_inicio < reserva_fin and hora_fin > reserva_inicio):
                        return reserva
        return None