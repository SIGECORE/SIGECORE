# app/service/reserva_aprobacion_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import AprobarReservaRequest
from repository.reserva_repository import ReservaRepository


class ReservaAprobacionService:

    def __init__(self, reserva_repo: ReservaRepository):
        self.reserva_repo = reserva_repo

    def listar_pendientes(self, usuario_autenticado: dict) -> list:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        return self.reserva_repo.get_pendientes()

    def aprobar_rechazar(self, reserva_id: int, data: AprobarReservaRequest, usuario_autenticado: dict) -> dict:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        estados_validos = ["aprobada", "rechazada"]
        if data.estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "ESTADO_INVALIDO",
                        "details": "El estado debe ser: aprobada o rechazada",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        reserva = self.reserva_repo.get_by_id(reserva_id)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Reserva no encontrada",
                    "error": {
                        "error_code": "RESERVA_NOT_FOUND",
                        "details": f"No existe una reserva con el ID {reserva_id}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        if reserva.estado != "pendiente":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "RESERVA_NO_PENDIENTE",
                        "details": f"La reserva ya fue procesada. Estado actual: {reserva.estado}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        reserva_actualizada = self.reserva_repo.aprobar_rechazar(
            reserva_id, data.estado, usuario_autenticado.get('id_usuario')
        )
        
        mensaje = "aprobada" if data.estado == "aprobada" else "rechazada"
        
        return {
            "success": True,
            "statusCode": 200,
            "message": f"Reserva {mensaje} exitosamente",
            "data": {
                "id_reserva": reserva_actualizada.id_reserva,
                "estado": reserva_actualizada.estado,
                "fecha_aprobacion": reserva_actualizada.fecha_aprobacion.isoformat(),
                "aprobado_por": f"Administrador (ID: {usuario_autenticado.get('id_usuario')})"
            }
        }