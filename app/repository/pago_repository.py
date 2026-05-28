# app/repository/pago_repository.py
from typing import Dict, Optional
from domain.models_domain import PagoResponse, EstadoPago
from datetime import datetime


class PagoRepository:
    
    def __init__(self):
        self._db: Dict[int, PagoResponse] = {}
        self._next_id: int = 1

    def guardar_pago(self, id_usuario: int, id_inmueble: int, monto: float, 
                    metodo_pago: str, comprobante_url: str) -> PagoResponse:
        
        pago = PagoResponse(
            id_pago=self._next_id,
            id_usuario=id_usuario,
            id_inmueble=id_inmueble,
            monto=monto,
            metodo_pago=metodo_pago,
            estado=EstadoPago.CONFIRMADO,
            fecha_pago=datetime.now(),
            comprobante_url=comprobante_url
        )
        self._db[self._next_id] = pago
        self._next_id += 1
        return pago