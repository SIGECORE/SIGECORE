# ==================== HU-007: Domain de Zonas Comunes ====================

class ErrorCode:
    ZONA_NOT_FOUND = "ZONA_NOT_FOUND"
    ZONA_NOMBRE_REQUERIDO = "ZONA_NOMBRE_REQUERIDO"
    ZONA_ESTADO_INVALIDO = "ZONA_ESTADO_INVALIDO"
    ZONA_CAPACIDAD_INVALIDA = "ZONA_CAPACIDAD_INVALIDA"

class ZonaDomain:
    
    @staticmethod
    def validar_nombre(nombre):
        """Validar que el nombre no esté vacío"""
        if not nombre or not nombre.strip():
            raise Exception(ErrorCode.ZONA_NOMBRE_REQUERIDO)
        return nombre.strip()
    
    @staticmethod
    def validar_capacidad(capacidad):
        """Validar que la capacidad sea positiva"""
        if capacidad is not None and capacidad <= 0:
            raise Exception(ErrorCode.ZONA_CAPACIDAD_INVALIDA)
        return capacidad
    
    @staticmethod
    def validar_estado(estado):
        """Validar que el estado sea válido"""
        estados_validos = ["disponible", "mantenimiento"]
        if estado and estado not in estados_validos:
            raise Exception(ErrorCode.ZONA_ESTADO_INVALIDO)
        return estado
    
    @staticmethod
    def existe_zona(zona, zona_id):
        """Validar que la zona existe"""
        if not zona:
            raise Exception(ErrorCode.ZONA_NOT_FOUND)
        return True