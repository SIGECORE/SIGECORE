# app/service/reserva_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import ReservaCreate, ReservaResponse


class ReservaService:

    def __init__(self, reserva_repo, zona_repo, usuario_repo):
        self.reserva_repo = reserva_repo
        self.zona_repo = zona_repo
        self.usuario_repo = usuario_repo

    def solicitar_reserva(self, data: ReservaCreate, usuario_autenticado: dict) -> ReservaResponse:
        
        id_usuario = usuario_autenticado.get('id_usuario')
        
        # Validar que el usuario esté activo
        usuario = self.usuario_repo.get_by_id(id_usuario)
        if not usuario or not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "No se puede realizar la reserva",
                    "error": {
                        "error_code": "USUARIO_INACTIVO",
                        "details": "El usuario no está activo",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que la zona existe
        zona = self.zona_repo.get_by_id(data.id_zona)
        if not zona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Zona no encontrada",
                    "error": {
                        "error_code": "ZONA_NOT_FOUND",
                        "details": f"No existe una zona con el ID {data.id_zona}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que la zona esté disponible
        if zona.estado != "disponible":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Zona no disponible",
                    "error": {
                        "error_code": "ZONA_MANTENIMIENTO",
                        "details": "La zona está en mantenimiento",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar fecha
        try:
            fecha_actual = datetime.now().date()
            fecha_reserva = datetime.strptime(data.fecha, "%Y-%m-%d").date()
            if fecha_reserva < fecha_actual:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "success": False,
                        "statusCode": 400,
                        "message": "Fecha inválida",
                        "error": {
                            "error_code": "FECHA_INVALIDA",
                            "details": "No se pueden reservar fechas pasadas",
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                )
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha inválido")
        
        # Validar horario
        if data.hora_inicio >= data.hora_fin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Horario inválido",
                    "error": {
                        "error_code": "HORARIO_INVALIDO",
                        "details": "La hora de inicio debe ser menor que la hora de fin",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar conflicto de horario
        if self.reserva_repo.hay_conflicto(data.id_zona, data.fecha, data.hora_inicio, data.hora_fin):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "success": False,
                    "statusCode": 409,
                    "message": "Conflicto de horario",
                    "error": {
                        "error_code": "RESERVA_CONFLICTO",
                        "details": "La zona ya está reservada en el horario solicitado",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Asegurar que nombre_usuario no sea None
        nombre_usuario = usuario_autenticado.get('nombre_completo')
        if not nombre_usuario:
            nombre_usuario = f"Usuario {id_usuario}"
        
        nombre_zona = zona.nombre
        
        return self.reserva_repo.create(data, id_usuario, nombre_usuario, nombre_zona)