from datetime import date, time, datetime
from typing import Tuple, Optional
from app.schemas import ConflictoInfo, DisponibilidadData

class ErrorCode:
    NO_AUTENTICADO = "NO_AUTENTICADO"
    ZONA_NOT_FOUND = "ZONA_NOT_FOUND"
    ZONA_MANTENIMIENTO = "ZONA_MANTENIMIENTO"
    FECHA_INVALIDA = "FECHA_INVALIDA"
    HORARIO_INVALIDO = "HORARIO_INVALIDO"
    PARAMETRO_REQUERIDO = "PARAMETRO_REQUERIDO"

class DisponibilidadDomain:
    
    @staticmethod
    def validar_parametros_obligatorios(zona_id, fecha, hora_inicio, hora_fin) -> Optional[Tuple[int, str, dict]]:
        """Validar que todos los parámetros obligatorios estén presentes"""
        if zona_id is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO, 
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO, 
                    "details": "El parámetro 'zona_id' es obligatorio"})
        if fecha is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO,
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO,
                    "details": "El parámetro 'fecha' es obligatorio"})
        if hora_inicio is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO,
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO,
                    "details": "El parámetro 'hora_inicio' es obligatorio"})
        if hora_fin is None:
            return (400, ErrorCode.PARAMETRO_REQUERIDO,
                   {"error_code": ErrorCode.PARAMETRO_REQUERIDO,
                    "details": "El parámetro 'hora_fin' es obligatorio"})
        return None
    
    @staticmethod
    def validar_fecha(fecha: date) -> Optional[Tuple[int, str, dict]]:
        """Validar que la fecha no sea anterior a hoy"""
        today = datetime.now().date()
        if fecha < today:
            return (400, ErrorCode.FECHA_INVALIDA,
                   {"error_code": ErrorCode.FECHA_INVALIDA,
                    "details": f"No se pueden consultar fechas pasadas. Fecha solicitada: {fecha}, Fecha actual: {today}"})
        return None
    
    @staticmethod
    def validar_horario(hora_inicio: time, hora_fin: time) -> Optional[Tuple[int, str, dict]]:
        """Validar que hora_inicio sea menor que hora_fin"""
        if hora_inicio >= hora_fin:
            return (400, ErrorCode.HORARIO_INVALIDO,
                   {"error_code": ErrorCode.HORARIO_INVALIDO,
                    "details": f"La hora de inicio ({hora_inicio}) debe ser menor que la hora de fin ({hora_fin})"})
        return None
    
    @staticmethod
    def construir_respuesta_disponible(zona, fecha, hora_inicio, hora_fin) -> DisponibilidadData:
        """Construir respuesta cuando la zona está disponible"""
        return DisponibilidadData(
            zona_id=zona.id,
            nombre=zona.nombre,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            disponible=True
        )
    
    @staticmethod
    def construir_respuesta_no_disponible(zona, fecha, hora_inicio, hora_fin, reserva_conflicto) -> DisponibilidadData:
        """Construir respuesta cuando la zona NO está disponible"""
        return DisponibilidadData(
            zona_id=zona.id,
            nombre=zona.nombre,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            disponible=False,
            conflicto_con=ConflictoInfo(
                id_reserva=reserva_conflicto.id,
                usuario=reserva_conflicto.usuario.nombre if reserva_conflicto.usuario else "Usuario",
                hora_inicio=reserva_conflicto.hora_inicio,
                hora_fin=reserva_conflicto.hora_fin
            )
        )