from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import date, time, datetime
from typing import Optional
from app.models import ZonaComun, Reserva, EstadoReservaEnum, Usuario

class ReservaRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_zona_by_id(self, zona_id: int) -> Optional[ZonaComun]:
        return self.db.query(ZonaComun).filter(ZonaComun.id == zona_id).first()
    
    def get_usuario_by_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def find_reserva_conflictiva(
        self, 
        zona_id: int, 
        fecha: date, 
        hora_inicio: time, 
        hora_fin: time
    ) -> Optional[Reserva]:
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
    
    def crear_reserva(
        self, 
        usuario_id: int,
        zona_id: int,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        observaciones: Optional[str] = None
    ) -> Reserva:
        nueva_reserva = Reserva(
            usuario_id=usuario_id,
            zona_id=zona_id,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estado=EstadoReservaEnum.PENDIENTE,
            observaciones=observaciones,
            fecha_solicitud=datetime.now()
        )
        self.db.add(nueva_reserva)
        self.db.commit()
        self.db.refresh(nueva_reserva)
        return nueva_reserva