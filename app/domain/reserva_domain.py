from datetime import date, time, datetime
from typing import Tuple, Optional

class ErrorCode:
    NO_AUTENTICADO = "NO_AUTENTICADO"
    ZONA_NOT_FOUND = "ZONA_NOT_FOUND"
    ZONA_MANTENIMIENTO = "ZONA_MANTENIMIENTO"
    FECHA_INVALIDA = "FECHA_INVALIDA"
    HORARIO_INVALIDO = "HORARIO_INVALIDO"
    RESERVA_CONFLICTO = "RESERVA_CONFLICTO"
    MOROSIDAD = "MOROSIDAD"
    USUARIO_INACTIVO = "USUARIO_INACTIVO"
    PARAMETRO_REQUERIDO = "PARAMETRO_REQUERIDO"

class ReservaDomain:
    
    @staticmethod
    def validar_parametros_obligatorios(id_zona, fecha, hora_inicio, hora_fin) -> Optional[Tuple[int, str, dict]]:
        if id_zona is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO,
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO,
                    "details": "El campo 'id_zona' es obligatorio"})
        if fecha is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO,
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO,
                    "details": "El campo 'fecha' es obligatorio"})
        if hora_inicio is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO,
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO,
                    "details": "El campo 'hora_inicio' es obligatorio"})
        if hora_fin is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO,
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO,
                    "details": "El campo 'hora_fin' es obligatorio"})
        return None
    
    @staticmethod
    def validar_fecha(fecha: date) -> Optional[Tuple[int, str, dict]]:
        today = datetime.now().date()
        if fecha < today:
            return (400, ErrorCode.FECHA_INVALIDA,
                   {"error_code": ErrorCode.FECHA_INVALIDA,
                    "details": f"No se pueden reservar fechas pasadas. Fecha solicitada: {fecha}"})
        return None
    
    @staticmethod
    def validar_horario(hora_inicio: time, hora_fin: time) -> Optional[Tuple[int, str, dict]]:
        if hora_inicio >= hora_fin:
            return (400, ErrorCode.HORARIO_INVALIDO,
                   {"error_code": ErrorCode.HORARIO_INVALIDO,
                    "details": f"La hora de inicio ({hora_inicio}) debe ser menor que la hora de fin ({hora_fin})"})
        return None
    
    @staticmethod
    def validar_usuario_activo(usuario) -> Optional[Tuple[int, str, dict]]:
        if not usuario.activo:
            return (400, ErrorCode.USUARIO_INACTIVO,
                   {"error_code": ErrorCode.USUARIO_INACTIVO,
                    "details": "El usuario no está activo en el sistema"})
        return None
    
    @staticmethod
    def validar_morosidad(usuario) -> Optional[Tuple[int, str, dict]]:
        if usuario.tiene_morosidad:
            return (400, ErrorCode.MOROSIDAD,
                   {"error_code": ErrorCode.MOROSIDAD,
                    "details": "El residente tiene pagos pendientes de cuotas de administración"})
        return None