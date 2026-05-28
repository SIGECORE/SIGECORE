# app/repository/inmueble_repository.py
from sqlalchemy.orm import Session
from models import Inmueble as InmuebleModel, AuditoriaInmueble, Usuario as UsuarioModel
from schemas import InmuebleCreate, EstadoInmueble, PropietarioInfo


class InmuebleRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, inmueble_id: int):
        return self.db.query(InmuebleModel).filter(InmuebleModel.id_inmueble == inmueble_id).first()

    def exists_by_numero_torre(self, numero: str, torre: str) -> bool:
        return self.db.query(InmuebleModel).filter(
            InmuebleModel.numero == numero, 
            InmuebleModel.torre == torre
        ).first() is not None

    def create(self, data: InmuebleCreate):
        db_inmueble = InmuebleModel(
            numero=data.numero,
            torre=data.torre,
            area_m2=data.area_m2,
            estado=EstadoInmueble.DISPONIBLE
        )
        self.db.add(db_inmueble)
        self.db.commit()
        self.db.refresh(db_inmueble)
        return db_inmueble

    def asignar_propietario(self, inmueble_id: int, id_propietario: int, id_usuario_modificador: int):
        inmueble = self.get_by_id(inmueble_id)
        if not inmueble:
            return None
        
        propietario_anterior = inmueble.id_propietario
        inmueble.id_propietario = id_propietario
        inmueble.estado = EstadoInmueble.OCUPADO
        
        # Registrar auditoría
        auditoria = AuditoriaInmueble(
            id_inmueble=inmueble_id,
            id_propietario_anterior=propietario_anterior,
            id_propietario_nuevo=id_propietario,
            id_usuario_modificador=id_usuario_modificador
        )
        self.db.add(auditoria)
        self.db.commit()
        self.db.refresh(inmueble)
        return inmueble

    def listar_con_filtros(self, torre: str = None, estado: str = None, nombre_propietario: str = None, 
                           page: int = 1, limit: int = 10):
        query = self.db.query(InmuebleModel)
        
        if torre:
            query = query.filter(InmuebleModel.torre == torre)
        if estado:
            query = query.filter(InmuebleModel.estado == estado)
        if nombre_propietario:
            query = query.join(UsuarioModel, InmuebleModel.id_propietario == UsuarioModel.id_usuario)
            query = query.filter(UsuarioModel.nombre_completo.contains(nombre_propietario))
        
        total = query.count()
        offset = (page - 1) * limit
        inmuebles = query.order_by(InmuebleModel.torre, InmuebleModel.numero).offset(offset).limit(limit).all()
        
        # Agregar información del propietario a cada inmueble
        for inmueble in inmuebles:
            if inmueble.id_propietario:
                usuario = self.db.query(UsuarioModel).filter(UsuarioModel.id_usuario == inmueble.id_propietario).first()
                if usuario:
                    inmueble.propietario = PropietarioInfo(
                        id_propietario=usuario.id_usuario,
                        nombre_completo=usuario.nombre_completo,
                        email=usuario.email,
                        telefono=usuario.telefono
                    )
        
        return inmuebles, total