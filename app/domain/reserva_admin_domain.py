from datetime import datetime
from typing import Tuple, Optional

class ErrorCode:
    NO_AUTENTICADO = "NO_AUTENTICADO"
    ACCESO_DENEGADO = "ACCESO_DENEGADO"
    RESERVA_NOT_FOUND = "RESERVA_NOT_FOUND"
    RESERVA_NO_PENDIENTE = "RESERVA_NO_PENDIENTE"
    ESTADO_INVALIDO = "ESTADO_INVALIDO"

class ReservaAdminDomain:
    
    @staticmethod
    def validar_administrador(usuario) -> Optional[Tuple[int, str, dict]]:
        """Validar que el usuario sea administrador"""
        if usuario.rol != "administrador":
            return (403, ErrorCode.ACCESO_DENEGADO,
                   {"error_code": ErrorCode.ACCESO_DENEGADO,
                    "details": "Se requiere rol de administrador para aprobar reservas"})
        return None
    
    @staticmethod
    def validar_estado_valido(estado: str) -> Optional[Tuple[int, str, dict]]:
        """Validar que el estado sea 'aprobada' o 'rechazada'"""
        if estado not in ["aprobada", "rechazada"]:
            return (400, ErrorCode.ESTADO_INVALIDO,
                   {"error_code": ErrorCode.ESTADO_INVALIDO,
                    "details": f"El estado '{estado}' no es válido. Debe ser 'aprobada' o 'rechazada'"})
        return None
    
    @staticmethod
    def validar_reserva_pendiente(reserva) -> Optional[Tuple[int, str, dict]]:
        """Validar que la reserva esté en estado pendiente"""
        if reserva.estado != "pendiente":
            return (400, ErrorCode.RESERVA_NO_PENDIENTE,
                   {"error_code": ErrorCode.RESERVA_NO_PENDIENTE,
                    "details": f"La reserva ya fue procesada anteriormente. Estado actual: {reserva.estado}"})
        return None