# app/repository/inmueble_repository.py
from sqlalchemy.orm import Session
from models import Inmueble as InmuebleModel


class InmuebleRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, inmueble_id: int):
        return self.db.query(InmuebleModel).filter(InmuebleModel.id_inmueble == inmueble_id).first()