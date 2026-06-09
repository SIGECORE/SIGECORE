# app/service/reserva_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import ReservaCreate, ReservaResponse


class ReservaService:

    def __init__(self, reserva_repo, zona_repo, usuario_repo):
        self.reserva_repo = reserva_repo
        self.zona_repo = zona_repo
        self.usuario_repo = usuario_repo

    # ==================== HU-009 (Solicitar reserva) ====================
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
        
        nombre_usuario = usuario_autenticado.get('nombre_completo')
        if not nombre_usuario:
            nombre_usuario = f"Usuario {id_usuario}"
        
        nombre_zona = zona.nombre
        
        return self.reserva_repo.create(data, id_usuario, nombre_usuario, nombre_zona)

    # ==================== HU-011 (Cancelar reserva) ====================
    def cancelar_reserva(self, reserva_id: int, usuario_autenticado: dict) -> dict:
        
        id_usuario_auth = usuario_autenticado.get('id_usuario')
        id_rol_auth = usuario_autenticado.get('id_rol')
        
        # Validar que la reserva existe
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
        
        # Validar que no esté cancelada
        if reserva.estado == "cancelada":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "RESERVA_YA_CANCELADA",
                        "details": "La reserva ya se encuentra cancelada",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que no esté rechazada
        if reserva.estado == "rechazada":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "RESERVA_RECHAZADA",
                        "details": "No se puede cancelar una reserva rechazada",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que la fecha no sea pasada
        try:
            fecha_reserva = datetime.strptime(reserva.fecha, "%Y-%m-%d").date()
            if fecha_reserva < datetime.now().date():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "success": False,
                        "statusCode": 400,
                        "message": "No se puede cancelar la reserva",
                        "error": {
                            "error_code": "FECHA_PASADA",
                            "details": "No se puede cancelar una reserva con fecha anterior a la actual",
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                )
        except ValueError:
            pass
        
        # Validar permisos
        es_propietario = (reserva.id_usuario == id_usuario_auth)
        es_admin = (id_rol_auth == 1)
        
        if not es_propietario and not es_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "NO_AUTORIZADO",
                        "details": "No tiene permisos para cancelar esta reserva",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar anticipación de 24 horas (solo para residentes)
        if not es_admin:
            try:
                fecha_reserva = datetime.strptime(reserva.fecha, "%Y-%m-%d")
                hora_inicio = datetime.strptime(reserva.hora_inicio, "%H:%M").time()
                datetime_reserva = datetime.combine(fecha_reserva.date(), hora_inicio)
                
                ahora = datetime.now()
                horas_anticipacion = (datetime_reserva - ahora).total_seconds() / 3600
                
                if horas_anticipacion < 24:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail={
                            "success": False,
                            "statusCode": 400,
                            "message": "No se puede cancelar la reserva",
                            "error": {
                                "error_code": "CANCELACION_TARDIA",
                                "details": "Las reservas solo se pueden cancelar con al menos 24 horas de anticipación",
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    )
            except:
                pass
        
        reserva_actualizada = self.reserva_repo.cancelar(reserva_id, id_usuario_auth)
        
        return {
            "success": True,
            "statusCode": 200,
            "message": "Reserva cancelada exitosamente",
            "data": {
                "id_reserva": reserva_actualizada.id_reserva,
                "id_zona": reserva_actualizada.id_zona,
                "nombre_zona": reserva_actualizada.nombre_zona,
                "fecha": reserva_actualizada.fecha,
                "hora_inicio": reserva_actualizada.hora_inicio,
                "hora_fin": reserva_actualizada.hora_fin,
                "estado": reserva_actualizada.estado,
                "fecha_cancelacion": reserva_actualizada.fecha_cancelacion.isoformat()
            }
        }

    # ==================== HU-012 (Consultar reservas por usuario) ====================
    def obtener_reservas_usuario(self, usuario_id: int, usuario_autenticado: dict) -> dict:
        
        id_usuario_auth = usuario_autenticado.get('id_usuario')
        id_rol_auth = usuario_autenticado.get('id_rol')
        
        # Validar que el usuario existe
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Usuario no encontrado",
                    "error": {
                        "error_code": "USUARIO_NOT_FOUND",
                        "details": f"No existe un usuario con el ID {usuario_id}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar permisos
        es_mismo_usuario = (id_usuario_auth == usuario_id)
        es_admin = (id_rol_auth == 1)
        
        if not es_mismo_usuario and not es_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "No tiene permisos para consultar las reservas de otro usuario",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        reservas = self.reserva_repo.get_reservas_by_usuario(usuario_id)
        
        reservas_con_zona = []
        for r in reservas:
            zona = self.zona_repo.get_by_id(r.id_zona)
            reservas_con_zona.append({
                "id_reserva": r.id_reserva,
                "zona": {
                    "id_zona": r.id_zona,
                    "nombre": zona.nombre if zona else f"Zona {r.id_zona}"
                },
                "fecha": r.fecha,
                "hora_inicio": r.hora_inicio,
                "hora_fin": r.hora_fin,
                "estado": r.estado,
                "fecha_solicitud": r.fecha_solicitud.isoformat()
            })
        
        mensaje = "Consulta exitosa" if reservas_con_zona else "El usuario no tiene reservas registradas"
        
        return {
            "success": True,
            "statusCode": 200,
            "message": mensaje,
            "data": {
                "usuario": {
                    "id_usuario": usuario.id_usuario,
                    "nombre_completo": usuario.nombre_completo,
                    "email": usuario.email
                },
                "reservas": reservas_con_zona
            }
        }