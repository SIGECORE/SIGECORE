# app/repository/pago_repository.py
from sqlalchemy.orm import Session
from models import Pago as PagoModel
from datetime import datetime


class PagoRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_ultimo_pago_by_inmueble(self, inmueble_id: int):
        return self.db.query(PagoModel).filter(
            PagoModel.id_inmueble == inmueble_id,
            PagoModel.estado == "confirmado"
        ).order_by(PagoModel.fecha_pago.desc()).first()
    
    def get_pagos_by_inmueble(self, inmueble_id: int):
        return self.db.query(PagoModel).filter(
            PagoModel.id_inmueble == inmueble_id,
            PagoModel.estado == "confirmado"
        ).order_by(PagoModel.fecha_pago.desc()).all()