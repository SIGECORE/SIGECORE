from sqlalchemy.orm import Session
from app.repository.reserva_admin_repository import ReservaAdminRepository
from app.domain.reserva_admin_domain import ReservaAdminDomain, ErrorCode

class ReservaAdminService:
    
    def __init__(self, db: Session):
        self.repository = ReservaAdminRepository(db)
    
    def listar_reservas_pendientes(self):
        """Listar todas las reservas pendientes"""
        reservas = self.repository.get_reservas_pendientes()
        
        resultado = []
        for reserva in reservas:
            usuario = self.repository.get_usuario_by_id(reserva.usuario_id)
            zona = self.repository.get_zona_by_id(reserva.zona_id)
            
            resultado.append({
                "id_reserva": reserva.id,
                "solicitante": {
                    "id_usuario": usuario.id,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "telefono": usuario.telefono
                },
                "zona": {
                    "id_zona": zona.id,
                    "nombre": zona.nombre
                },
                "fecha": reserva.fecha,
                "hora_inicio": reserva.hora_inicio,
                "hora_fin": reserva.hora_fin,
                "observaciones": reserva.observaciones,
                "fecha_solicitud": reserva.fecha_solicitud
            })
        
        return resultado
    
    def cambiar_estado_reserva(
        self,
        reserva_id: int,
        nuevo_estado: str,
        administrador_id: int
    ):
        # Validar que la reserva existe
        reserva = self.repository.get_reserva_by_id(reserva_id)
        if not reserva:
            raise Exception(ErrorCode.RESERVA_NOT_FOUND)
        
        # Validar que la reserva está pendiente
        error = ReservaAdminDomain.validar_reserva_pendiente(reserva)
        if error:
            raise Exception(error[1])
        
        # Si es aprobada, verificar disponibilidad nuevamente (evitar conflictos)
        if nuevo_estado == "aprobada":
            disponible = self.repository.verificar_disponibilidad_aprobacion(
                reserva.zona_id,
                reserva.fecha,
                reserva.hora_inicio,
                reserva.hora_fin,
                reserva.id
            )
            if not disponible:
                raise Exception(ErrorCode.RESERVA_CONFLICTO)
        
        # Actualizar estado
        reserva_actualizada = self.repository.actualizar_estado_reserva(
            reserva, nuevo_estado, administrador_id
        )
        
        # Obtener datos del administrador
        administrador = self.repository.get_usuario_by_id(administrador_id)
        
        return {
            "id_reserva": reserva_actualizada.id,
            "estado": reserva_actualizada.estado,
            "fecha_aprobacion": reserva_actualizada.fecha_aprobacion,
            "aprobado_por": f"{administrador.nombre} (ID: {administrador.id})"
        }