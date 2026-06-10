# app/repository/reserva_repository.py
from typing import Dict, Optional, List
from domain.models_domain import ReservaResponse, ReservaCreate
from datetime import datetime


class ReservaRepository:

    def __init__(self):
        self._db: Dict[int, ReservaResponse] = {}
        self._next_id: int = 1

    # ==================== HU-009 (Crear reserva) ====================
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

    def get_pendientes(self) -> List[ReservaResponse]:
        pendientes = []
        for reserva in self._db.values():
            if reserva.estado == "pendiente":
                pendientes.append(reserva)
        return pendientes

    def hay_conflicto(self, zona_id: int, fecha: str, hora_inicio: str, hora_fin: str) -> bool:
        for reserva in self._db.values():
            if reserva.id_zona == zona_id and reserva.fecha == fecha:
                if reserva.estado == "aprobada":
                    if (hora_inicio < reserva.hora_fin and hora_fin > reserva.hora_inicio):
                        return True
        return False

    # ==================== HU-010 (Aprobar/Rechazar reserva) ====================
    def aprobar_rechazar(self, reserva_id: int, estado: str, id_administrador: int) -> Optional[ReservaResponse]:
        reserva = self._db.get(reserva_id)
        if not reserva:
            return None
        
        if reserva.estado != "pendiente":
            return None
        
        reserva.estado = estado
        reserva.fecha_aprobacion = datetime.now()
        reserva.aprobado_por = id_administrador
        
        return reserva

    # ==================== HU-011 (Cancelar reserva) ====================
    def cancelar(self, reserva_id: int, id_usuario: int) -> Optional[ReservaResponse]:
        reserva = self._db.get(reserva_id)
        if not reserva:
            return None
        
        if reserva.estado == "cancelada":
            return None
        
        if reserva.estado == "rechazada":
            return None
        
        reserva.estado = "cancelada"
        reserva.fecha_cancelacion = datetime.now()
        reserva.cancelado_por = id_usuario
        
        return reserva

    # ==================== HU-012 (Consultar reservas por usuario) ====================
    def get_reservas_by_usuario(self, usuario_id: int) -> List[ReservaResponse]:
        reservas = []
        for reserva in self._db.values():
            if reserva.id_usuario == usuario_id:
                reservas.append(reserva)
        # Ordenar por fecha descendente
        reservas.sort(key=lambda x: x.fecha, reverse=True)
        return reservas