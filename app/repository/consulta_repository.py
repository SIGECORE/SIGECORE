from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from app.models import Usuario, Reserva, ZonaComun

class ConsultaRepository:
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_usuario_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtener usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def get_reservas_by_usuario_id(self, usuario_id: int) -> List[Reserva]:
        """Obtener reservas de un usuario ordenadas por fecha descendente"""
        return self.db.query(Reserva).filter(
            Reserva.usuario_id == usuario_id
        ).order_by(desc(Reserva.fecha)).all()
    
    def get_zona_by_id(self, zona_id: int) -> Optional[ZonaComun]:
        """Obtener zona por ID"""
        return self.db.query(ZonaComun).filter(ZonaComun.id == zona_id).first()