from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.models import Reserva, Usuario, ZonaComun

class CancelacionRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_reserva_by_id(self, reserva_id: int) -> Optional[Reserva]:
        """Obtener reserva por ID"""
        return self.db.query(Reserva).filter(Reserva.id == reserva_id).first()
    
    def get_usuario_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def get_zona_by_id(self, zona_id: int) -> Optional[ZonaComun]:
        """Obtener zona por ID"""
        return self.db.query(ZonaComun).filter(ZonaComun.id == zona_id).first()
    
    def cancelar_reserva(self, reserva: Reserva, usuario_id: int) -> Reserva:
        """Cancelar reserva"""
        reserva.estado = "cancelada"
        reserva.fecha_cancelacion = datetime.now()
        reserva.cancelado_por = usuario_id
        self.db.commit()
        self.db.refresh(reserva)
        return reserva