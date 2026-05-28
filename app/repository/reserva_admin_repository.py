from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import Optional, List
from app.models import Reserva, Usuario, ZonaComun, EstadoReservaEnum

class ReservaAdminRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_reservas_pendientes(self) -> List[Reserva]:
        """Obtener todas las reservas con estado pendiente"""
        return self.db.query(Reserva).filter(
            Reserva.estado == EstadoReservaEnum.PENDIENTE
        ).order_by(Reserva.fecha_solicitud.desc()).all()
    
    def get_reserva_by_id(self, reserva_id: int) -> Optional[Reserva]:
        """Obtener reserva por ID"""
        return self.db.query(Reserva).filter(Reserva.id == reserva_id).first()
    
    def get_usuario_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def get_zona_by_id(self, zona_id: int) -> Optional[ZonaComun]:
        """Obtener zona por ID"""
        return self.db.query(ZonaComun).filter(ZonaComun.id == zona_id).first()
    
    def actualizar_estado_reserva(
        self, 
        reserva: Reserva, 
        nuevo_estado: str, 
        administrador_id: int
    ) -> Reserva:
        """Actualizar el estado de una reserva"""
        reserva.estado = nuevo_estado
        reserva.fecha_aprobacion = datetime.now()
        reserva.aprobado_por = administrador_id
        self.db.commit()
        self.db.refresh(reserva)
        return reserva
    
    def verificar_disponibilidad_aprobacion(
        self, 
        zona_id: int, 
        fecha, 
        hora_inicio, 
        hora_fin,
        reserva_id_actual: int
    ) -> bool:
        """Verificar disponibilidad para aprobar (evitar conflictos)"""
        conflicto = self.db.query(Reserva).filter(
            and_(
                Reserva.zona_id == zona_id,
                Reserva.fecha == fecha,
                Reserva.estado == EstadoReservaEnum.APROBADA,
                Reserva.id != reserva_id_actual,
                Reserva.hora_inicio < hora_fin,
                Reserva.hora_fin > hora_inicio
            )
        ).first()
        return conflicto is None