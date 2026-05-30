from datetime import datetime

class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password=None, rol="residente", activo=True):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.rol = rol
        self.activo = activo

class ZonaComun:
    def __init__(self, id=None, nombre=None, capacidad_maxima=None, descripcion=None,
                 estado="disponible", horario_inicio=None, horario_fin=None, fecha_registro=None):
        self.id = id
        self.nombre = nombre
        self.capacidad_maxima = capacidad_maxima
        self.descripcion = descripcion
        self.estado = estado
        self.horario_inicio = horario_inicio
        self.horario_fin = horario_fin
        self.fecha_registro = fecha_registro or datetime.now()