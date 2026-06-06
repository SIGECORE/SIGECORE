# app/repository/pago_repository.py
from typing import Dict, List, Optional
from domain.models_domain import PagoResponse, EstadoPago
from datetime import datetime


class PagoRepository:

    def __init__(self):
        self._db: Dict[int, PagoResponse] = {}
        self._next_id: int = 1

    # ==================== HU-015 (Registro de pago) ====================
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

    # ==================== HU-016 (Historial de pagos por usuario) ====================
    def get_pagos_by_usuario(self, usuario_id: int) -> List[PagoResponse]:
        pagos = []
        for pago in self._db.values():
            if pago.id_usuario == usuario_id:
                pagos.append(pago)
        pagos.sort(key=lambda x: x.fecha_pago, reverse=True)
        return pagos

    # ==================== HU-017 (Reporte de cartera) ====================
    def get_ultimo_pago_by_inmueble(self, inmueble_id: int) -> Optional[PagoResponse]:
        ultimo = None
        for pago in self._db.values():
            if pago.id_inmueble == inmueble_id:
                if ultimo is None or pago.fecha_pago > ultimo.fecha_pago:
                    ultimo = pago
        return ultimo

    def get_all_pagos(self) -> List[PagoResponse]:
        return list(self._db.values())