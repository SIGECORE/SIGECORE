from app.repository.zona_repository import ZonaRepository
from app.domain.zona_domain import ZonaDomain, ErrorCode

class ZonaService:
    
    def __init__(self):
        self.repository = ZonaRepository()
    
    def listar_zonas(self):
        """Listar todas las zonas"""
        zonas = self.repository.get_all()
        return [dict(zona) for zona in zonas]
    
    def obtener_zona(self, zona_id):
        """Obtener una zona por ID"""
        zona = self.repository.get_by_id(zona_id)
        if not zona:
            return None
        return dict(zona)
    
    def crear_zona(self, nombre, descripcion, capacidad):
        """Crear una nueva zona"""
        # Validaciones del domain
        nombre = ZonaDomain.validar_nombre(nombre)
        capacidad = ZonaDomain.validar_capacidad(capacidad)
        
        zona_id = self.repository.create(nombre, descripcion, capacidad)
        return self.obtener_zona(zona_id)
    
    def actualizar_zona(self, zona_id, nombre=None, descripcion=None, capacidad=None, estado=None):
        """Actualizar una zona"""
        # Validar que existe
        zona = self.repository.get_by_id(zona_id)
        ZonaDomain.existe_zona(zona, zona_id)
        
        # Validaciones del domain
        if nombre:
            nombre = ZonaDomain.validar_nombre(nombre)
        if capacidad:
            capacidad = ZonaDomain.validar_capacidad(capacidad)
        if estado:
            estado = ZonaDomain.validar_estado(estado)
        
        self.repository.update(zona_id, nombre, descripcion, capacidad, estado)
        return self.obtener_zona(zona_id)
    
    def eliminar_zona(self, zona_id):
        """Eliminar una zona"""
        # Validar que existe
        zona = self.repository.get_by_id(zona_id)
        ZonaDomain.existe_zona(zona, zona_id)
        
        return self.repository.delete(zona_id)