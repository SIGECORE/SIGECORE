from sqlalchemy.orm import Session
from app.repository.cancelacion_repository import CancelacionRepository
from app.domain.cancelacion_domain import CancelacionDomain, ErrorCode

class CancelacionService:
    
    def __init__(self, db: Session):
        self.repository = CancelacionRepository(db)
    
    def cancelar_reserva(
        self,
        reserva_id: int,
        usuario_id: int,
        usuario_rol: str
    ):
        # Validar que la reserva existe
        reserva = self.repository.get_reserva_by_id(reserva_id)
        if not reserva:
            raise Exception(ErrorCode.RESERVA_NOT_FOUND)
        
        # Validar autorización (propietario o administrador)
        error = CancelacionDomain.validar_autorizacion(reserva, usuario_id, usuario_rol)
        if error:
            raise Exception(error[1])
        
        # Validar que no esté cancelada
        error = CancelacionDomain.validar_reserva_no_cancelada(reserva)
        if error:
            raise Exception(error[1])
        
        # Validar que no esté rechazada
        error = CancelacionDomain.validar_reserva_no_rechazada(reserva)
        if error:
            raise Exception(error[1])
        
        # Validar fecha no pasada
        error = CancelacionDomain.validar_fecha_no_pasada(reserva)
        if error:
            raise Exception(error[1])
        
        # Validar anticipación de 24 horas (solo para residentes)
        error = CancelacionDomain.validar_anticipacion_24h(reserva, usuario_rol)
        if error:
            raise Exception(error[1])
        
        # Cancelar reserva
        reserva_cancelada = self.repository.cancelar_reserva(reserva, usuario_id)
        
        # Obtener zona
        zona = self.repository.get_zona_by_id(reserva_cancelada.zona_id)
        
        return {
            "id_reserva": reserva_cancelada.id,
            "id_zona": reserva_cancelada.zona_id,
            "nombre_zona": zona.nombre,
            "fecha": reserva_cancelada.fecha,
            "hora_inicio": reserva_cancelada.hora_inicio,
            "hora_fin": reserva_cancelada.hora_fin,
            "estado": reserva_cancelada.estado,
            "fecha_cancelacion": reserva_cancelada.fecha_cancelacion
        }