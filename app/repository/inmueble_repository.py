# app/repository/inmueble_repository.py
from sqlalchemy.orm import Session
from models import Inmueble as InmuebleModel


class InmuebleRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_all_inmuebles(self):
        return self.db.query(InmuebleModel).all()
    
    def get_by_torre(self, torre: str):
        return self.db.query(InmuebleModel).filter(InmuebleModel.torre == torre).all()