from app.repository.zona_repository import ZonaRepository
from app.domain.zona_domain import ZonaDomain, ErrorCode

class ZonaService:
    
    def __init__(self):
        self.repository = ZonaRepository()
    
    def registrar_zona(self, nombre, capacidad_maxima, descripcion, horario_inicio, horario_fin, usuario_actual):
        """Registrar una nueva zona común"""
        
        # Validar que sea administrador
        ZonaDomain.validar_administrador(usuario_actual)
        
        # Validar campos requeridos
        ZonaDomain.validar_campos_requeridos(nombre, capacidad_maxima)
        
        # Validar capacidad
        capacidad_maxima = ZonaDomain.validar_capacidad(capacidad_maxima)
        
        # Validar nombre único
        zona_existente = self.repository.get_by_nombre(nombre)
        ZonaDomain.validar_nombre_unico(zona_existente, nombre)
        
        # Crear zona
        zona = self.repository.create(nombre, capacidad_maxima, descripcion, horario_inicio, horario_fin)
        
        return {
            "id_zona": zona["id"],
            "nombre": zona["nombre"],
            "capacidad_maxima": zona["capacidad_maxima"],
            "descripcion": zona["descripcion"],
            "estado": zona["estado"],
            "horario_inicio": zona["horario_inicio"],
            "horario_fin": zona["horario_fin"],
            "fecha_registro": zona["fecha_registro"]
        }