from datetime import datetime, timedelta
from typing import Tuple, Optional

class ErrorCode:
    NO_AUTENTICADO = "NO_AUTENTICADO"
    RESERVA_NOT_FOUND = "RESERVA_NOT_FOUND"
    RESERVA_YA_CANCELADA = "RESERVA_YA_CANCELADA"
    RESERVA_RECHAZADA = "RESERVA_RECHAZADA"
    CANCELACION_TARDIA = "CANCELACION_TARDIA"
    FECHA_PASADA = "FECHA_PASADA"
    NO_AUTORIZADO = "NO_AUTORIZADO"

class CancelacionDomain:
    
    @staticmethod
    def validar_autorizacion(reserva, usuario_id, usuario_rol) -> Optional[Tuple[int, str, dict]]:
        """Validar que el usuario sea propietario o administrador"""
        if usuario_rol != "administrador" and reserva.usuario_id != usuario_id:
            return (403, ErrorCode.NO_AUTORIZADO,
                   {"error_code": ErrorCode.NO_AUTORIZADO,
                    "details": "No tiene permiso para cancelar esta reserva"})
        return None
    
    @staticmethod
    def validar_reserva_no_cancelada(reserva) -> Optional[Tuple[int, str, dict]]:
        """Validar que la reserva no esté cancelada"""
        if reserva.estado == "cancelada":
            return (400, ErrorCode.RESERVA_YA_CANCELADA,
                   {"error_code": ErrorCode.RESERVA_YA_CANCELADA,
                    "details": "La reserva ya se encuentra cancelada"})
        return None
    
    @staticmethod
    def validar_reserva_no_rechazada(reserva) -> Optional[Tuple[int, str, dict]]:
        """Validar que la reserva no esté rechazada"""
        if reserva.estado == "rechazada":
            return (400, ErrorCode.RESERVA_RECHAZADA,
                   {"error_code": ErrorCode.RESERVA_RECHAZADA,
                    "details": "No se puede cancelar una reserva que ya fue rechazada"})
        return None
    
    @staticmethod
    def validar_fecha_no_pasada(reserva) -> Optional[Tuple[int, str, dict]]:
        """Validar que la fecha de la reserva no sea anterior a hoy"""
        today = datetime.now().date()
        if reserva.fecha < today:
            return (400, ErrorCode.FECHA_PASADA,
                   {"error_code": ErrorCode.FECHA_PASADA,
                    "details": "No se puede cancelar una reserva con fecha pasada"})
        return None
    
    @staticmethod
    def validar_anticipacion_24h(reserva, usuario_rol) -> Optional[Tuple[int, str, dict]]:
        """Validar que la cancelación tenga al menos 24 horas de anticipación (solo para residentes)"""
        if usuario_rol == "administrador":
            return None
        
        ahora = datetime.now()
        fecha_hora_reserva = datetime.combine(reserva.fecha, reserva.hora_inicio)
        diferencia = fecha_hora_reserva - ahora
        
        if diferencia < timedelta(hours=24):
            return (400, ErrorCode.CANCELACION_TARDIA,
                   {"error_code": ErrorCode.CANCELACION_TARDIA,
                    "details": f"Las reservas solo se pueden cancelar con al menos 24 horas de anticipación. Faltan {int(diferencia.total_seconds() / 3600)} horas"})
        return None