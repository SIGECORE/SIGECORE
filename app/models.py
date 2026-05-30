from datetime import datetime

class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password=None, 
                 telefono=None, rol="residente", activo=True, tiene_morosidad=False):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.telefono = telefono
        self.rol = rol
        self.activo = activo
        self.tiene_morosidad = tiene_morosidad

class ZonaComun:
    def __init__(self, id=None, nombre=None, descripcion=None, capacidad=None, estado="disponible"):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.capacidad = capacidad
        self.estado = estado

class Reserva:
    def __init__(self, id=None, zona_id=None, usuario_id=None, fecha=None,
                 hora_inicio=None, hora_fin=None, estado="pendiente", observaciones=None,
                 fecha_solicitud=None, fecha_aprobacion=None, aprobado_por=None,
                 fecha_cancelacion=None, cancelado_por=None):
        self.id = id
        self.zona_id = zona_id
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
        self.observaciones = observaciones
        self.fecha_solicitud = fecha_solicitud or datetime.now()
        self.fecha_aprobacion = fecha_aprobacion
        self.aprobado_por = aprobado_por
        self.fecha_cancelacion = fecha_cancelacion
        self.cancelado_por = cancelado_por