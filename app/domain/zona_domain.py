# ==================== HU-007: Domain de Zonas Comunes ====================

class ErrorCode:
    NO_AUTENTICADO = "NO_AUTENTICADO"
    ACCESO_DENEGADO = "ACCESO_DENEGADO"
    ZONA_DUPLICADA = "ZONA_DUPLICADA"
    CAPACIDAD_INVALIDA = "CAPACIDAD_INVALIDA"
    CAMPO_REQUERIDO = "CAMPO_REQUERIDO"

class ZonaDomain:
    
    @staticmethod
    def validar_administrador(usuario):
        """Validar que el usuario sea administrador"""
        if not usuario:
            raise Exception(ErrorCode.NO_AUTENTICADO)
        if usuario.get("rol") != "administrador":
            raise Exception(ErrorCode.ACCESO_DENEGADO)
        return True
    
    @staticmethod
    def validar_campos_requeridos(nombre, capacidad_maxima):
        """Validar que los campos obligatorios estén presentes"""
        if not nombre or not nombre.strip():
            raise Exception(ErrorCode.CAMPO_REQUERIDO)
        if capacidad_maxima is None:
            raise Exception(ErrorCode.CAMPO_REQUERIDO)
        return True
    
    @staticmethod
    def validar_capacidad(capacidad_maxima):
        """Validar que la capacidad sea un entero positivo"""
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise Exception(ErrorCode.CAPACIDAD_INVALIDA)
        return capacidad_maxima
    
    @staticmethod
    def validar_nombre_unico(zona_existente, nombre):
        """Validar que el nombre de la zona no esté duplicado"""
        if zona_existente:
            raise Exception(ErrorCode.ZONA_DUPLICADA)
        return True