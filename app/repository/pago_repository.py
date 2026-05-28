# app/repository/pago_repository.py
from sqlalchemy.orm import Session
from models import Pago as PagoModel, Inmueble as InmuebleModel
from domain.models_domain import InmuebleInfo


class PagoRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_pagos_by_usuario(self, usuario_id: int):
        resultados = self.db.query(
            PagoModel,
            InmuebleModel.numero,
            InmuebleModel.torre
        ).join(
            InmuebleModel, PagoModel.id_inmueble == InmuebleModel.id_inmueble
        ).filter(
            PagoModel.id_usuario == usuario_id
        ).order_by(
            PagoModel.fecha_pago.desc()
        ).all()
        
        pagos = []
        for pago, numero, torre in resultados:
            pagos.append(
                PagoResponse(
                    id_pago=pago.id_pago,
                    inmueble=InmuebleInfo(
                        id_inmueble=pago.id_inmueble,
                        numero=numero,
                        torre=torre
                    ),
                    monto=pago.monto,
                    metodo_pago=pago.metodo_pago,
                    estado=pago.estado.value,
                    fecha_pago=pago.fecha_pago,
                    comprobante_url=pago.comprobante_url
                )
            )
        
        return pagos