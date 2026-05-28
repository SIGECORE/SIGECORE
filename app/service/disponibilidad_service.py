from sqlalchemy.orm import Session
from app.repository.disponibilidad_repository import DisponibilidadRepository
from app.domain.disponibilidad_domain import DisponibilidadDomain, ErrorCode
from app.models import EstadoZonaEnum

class DisponibilidadService:
    
    def __init__(self, db: Session):
        self.repository = DisponibilidadRepository(db)
    
    def verificar_disponibilidad(
        self, 
        zona_id: int, 
        fecha, 
        hora_inicio, 
        hora_fin
    ):
        # Validar zona existe
        zona = self.repository.get_zona_by_id(zona_id)
        if not zona:
            raise Exception(ErrorCode.ZONA_NOT_FOUND)
        
        # Validar zona no está en mantenimiento
        if zona.estado != EstadoZonaEnum.DISPONIBLE:
            raise Exception(ErrorCode.ZONA_MANTENIMIENTO)
        
        # Buscar reserva conflictiva
        reserva_conflicto = self.repository.find_reserva_conflictiva(
            zona_id, fecha, hora_inicio, hora_fin
        )
        
        # Construir respuesta según disponibilidad
        if reserva_conflicto is None:
            return DisponibilidadDomain.construir_respuesta_disponible(
                zona, fecha, hora_inicio, hora_fin
            )
        else:
            return DisponibilidadDomain.construir_respuesta_no_disponible(
                zona, fecha, hora_inicio, hora_fin, reserva_conflicto
            )