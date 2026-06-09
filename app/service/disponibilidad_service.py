# app/service/disponibilidad_service.py
from datetime import datetime
from fastapi import HTTPException, status
from repository.zona_repository import ZonaRepository
from repository.reserva_repository import ReservaRepository
from domain.models_domain import (
    DisponibilidadResponse, DisponibilidadData, ConflictoInfo
)


class DisponibilidadService:

    def __init__(self, zona_repo: ZonaRepository, reserva_repo: ReservaRepository):
        self.zona_repo = zona_repo
        self.reserva_repo = reserva_repo

    def consultar_disponibilidad(self, usuario_autenticado: dict, zona_id: int, fecha: str,
                                  hora_inicio: str, hora_fin: str) -> DisponibilidadResponse:
        
        # Validar que la zona existe
        zona = self.zona_repo.get_by_id(zona_id)
        if not zona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Zona no encontrada",
                    "error": {
                        "error_code": "ZONA_NOT_FOUND",
                        "details": f"No existe una zona común con el ID {zona_id}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que la zona esté disponible (no en mantenimiento)
        if zona.estado != "disponible":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Zona no disponible",
                    "error": {
                        "error_code": "ZONA_MANTENIMIENTO",
                        "details": "La zona común está actualmente en mantenimiento y no puede ser reservada",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Verificar conflictos con reservas existentes
        conflicto = self.reserva_repo.hay_conflicto(zona_id, fecha, hora_inicio, hora_fin)
        
        if conflicto:
            return DisponibilidadResponse(
                success=True,
                statusCode=200,
                message="La zona no está disponible en el horario solicitado",
                data=DisponibilidadData(
                    zona_id=zona_id,
                    nombre=zona.nombre,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    disponible=False,
                    conflicto_con=ConflictoInfo(
                        id_reserva=conflicto.get("id_reserva"),
                        usuario=f"Usuario {conflicto.get('usuario_id', 'desconocido')}",
                        hora_inicio=conflicto.get("hora_inicio"),
                        hora_fin=conflicto.get("hora_fin")
                    )
                )
            )
        else:
            return DisponibilidadResponse(
                success=True,
                statusCode=200,
                message="La zona está disponible",
                data=DisponibilidadData(
                    zona_id=zona_id,
                    nombre=zona.nombre,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    disponible=True,
                    conflicto_con=None
                )
            )