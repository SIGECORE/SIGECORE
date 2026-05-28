from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, time
from typing import Optional
from app.models import ZonaComun, Reserva, EstadoReservaEnum

class DisponibilidadRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_zona_by_id(self, zona_id: int) -> Optional[ZonaComun]:
        """Obtener zona por ID"""
        return self.db.query(ZonaComun).filter(ZonaComun.id == zona_id).first()
    
    def find_reserva_conflictiva(
        self, 
        zona_id: int, 
        fecha: date, 
        hora_inicio: time, 
        hora_fin: time
    ) -> Optional[Reserva]:
        """Buscar reserva conflictiva aprobada"""
        conflicto = self.db.query(Reserva).filter(
            and_(
                Reserva.zona_id == zona_id,
                Reserva.fecha == fecha,
                Reserva.estado == EstadoReservaEnum.APROBADA,
                Reserva.hora_inicio < hora_fin,
                Reserva.hora_fin > hora_inicio
            )
        ).first()
        
        return conflicto