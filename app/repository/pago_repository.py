# app/repository/pago_repository.py
from sqlalchemy.orm import Session
from models import Pago as PagoModel
from schemas import EstadoPago


class PagoRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def guardar_pago(self, id_usuario: int, id_inmueble: int, monto: float, 
                     metodo_pago: str, comprobante_url: str) -> PagoModel:
        
        db_pago = PagoModel(
            id_usuario=id_usuario,
            id_inmueble=id_inmueble,
            monto=monto,
            metodo_pago=metodo_pago,
            estado=EstadoPago.CONFIRMADO,
            comprobante_url=comprobante_url
        )
        self.db.add(db_pago)
        self.db.commit()
        self.db.refresh(db_pago)
        return db_pago