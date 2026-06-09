from sqlalchemy.orm import Session
from app.repository.consulta_repository import ConsultaRepository
from app.domain.consulta_domain import ConsultaDomain, ErrorCode

class ConsultaService:
    
    def __init__(self, db: Session):
        self.repository = ConsultaRepository(db)
    
    def consultar_reservas_usuario(
        self,
        usuario_consultado_id: int,
        usuario_autenticado_id: int,
        usuario_autenticado_rol: str
    ):
        # Validar que el usuario consultado existe
        usuario = self.repository.get_usuario_by_id(usuario_consultado_id)
        if not usuario:
            raise Exception(ErrorCode.USUARIO_NOT_FOUND)
        
        # Validar permisos de acceso
        error = ConsultaDomain.validar_acceso(
            usuario_autenticado_id, 
            usuario_autenticado_rol, 
            usuario_consultado_id
        )
        if error:
            raise Exception(error[1])
        
        # Obtener reservas del usuario
        reservas = self.repository.get_reservas_by_usuario_id(usuario_consultado_id)
        
        # Construir respuesta
        reservas_list = []
        for reserva in reservas:
            zona = self.repository.get_zona_by_id(reserva.zona_id)
            reservas_list.append({
                "id_reserva": reserva.id,
                "zona": {
                    "id_zona": zona.id,
                    "nombre": zona.nombre
                },
                "fecha": reserva.fecha,
                "hora_inicio": reserva.hora_inicio,
                "hora_fin": reserva.hora_fin,
                "estado": reserva.estado,
                "fecha_solicitud": reserva.fecha_solicitud
            })
        
        return {
            "usuario": {
                "id_usuario": usuario.id,
                "nombre_completo": usuario.nombre,
                "email": usuario.email
            },
            "reservas": reservas_list
        }