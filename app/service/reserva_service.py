from sqlalchemy.orm import Session
from app.repository.reserva_repository import ReservaRepository
from app.domain.reserva_domain import ReservaDomain, ErrorCode

class ReservaService:
    
    def __init__(self, db: Session):
        self.repository = ReservaRepository(db)
    
    def crear_solicitud_reserva(
        self,
        usuario_id: int,
        id_zona: int,
        fecha,
        hora_inicio,
        hora_fin,
        observaciones: str = None
    ):
        # Validar usuario
        usuario = self.repository.get_usuario_by_id(usuario_id)
        if not usuario:
            raise Exception(ErrorCode.USUARIO_INACTIVO)
        
        error = ReservaDomain.validar_usuario_activo(usuario)
        if error:
            raise Exception(error[1])
        
        error = ReservaDomain.validar_morosidad(usuario)
        if error:
            raise Exception(error[1])
        
        # Validar zona
        zona = self.repository.get_zona_by_id(id_zona)
        if not zona:
            raise Exception(ErrorCode.ZONA_NOT_FOUND)
        
        if zona.estado != "disponible":
            raise Exception(ErrorCode.ZONA_MANTENIMIENTO)
        
        # Validar conflicto
        reserva_conflicto = self.repository.find_reserva_conflictiva(
            id_zona, fecha, hora_inicio, hora_fin
        )
        if reserva_conflicto:
            raise Exception(ErrorCode.RESERVA_CONFLICTO)
        
        # Crear reserva
        nueva_reserva = self.repository.crear_reserva(
            usuario_id=usuario_id,
            zona_id=id_zona,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            observaciones=observaciones
        )
        
        return {
            "id_reserva": nueva_reserva.id,
            "id_usuario": nueva_reserva.usuario_id,
            "nombre_usuario": usuario.nombre,
            "id_zona": nueva_reserva.zona_id,
            "nombre_zona": zona.nombre,
            "fecha": nueva_reserva.fecha,
            "hora_inicio": nueva_reserva.hora_inicio,
            "hora_fin": nueva_reserva.hora_fin,
            "estado": nueva_reserva.estado,
            "fecha_solicitud": nueva_reserva.fecha_solicitud
        }