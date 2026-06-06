# app/service/pago_service.py
import random
from fastapi import HTTPException, status
from domain.models_domain import (
    PagoRequest, PagoResponse, HistorialPagosResponse,
    UsuarioInfo, PagoHistorialResponse, InmuebleInfo
)
from repository.pago_repository import PagoRepository
from repository.inmueble_repository import InmuebleRepository


def procesar_pago_externo(monto: float, metodo_pago: str, token: str) -> bool:
    return random.random() < 0.8


class PagoService:

    def __init__(self, pago_repo: PagoRepository, inmueble_repo: InmuebleRepository):
        self.pago_repo = pago_repo
        self.inmueble_repo = inmueble_repo

    def registrar_pago(self, data: PagoRequest, usuario_autenticado: dict) -> PagoResponse:
        
        id_usuario = usuario_autenticado.get('id_usuario')
        id_rol = usuario_autenticado.get('id_rol')
        
        if not data.id_inmueble or not data.monto or not data.metodo_pago:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los campos id_inmueble, monto y metodo_pago son obligatorios"
            )
        
        if data.monto <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El monto debe ser mayor a 0"
            )
        
        inmueble = self.inmueble_repo.get_by_id(data.id_inmueble)
        if not inmueble:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un inmueble con el ID {data.id_inmueble}"
            )
        
        es_propietario = inmueble.id_propietario == id_usuario
        es_admin = (id_rol == 1)
        
        if not es_propietario and not es_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No es propietario del inmueble asociado al pago"
            )
        
        if not procesar_pago_externo(data.monto, data.metodo_pago, data.token_pasarela):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="La pasarela de pagos no está disponible en este momento"
            )
        
        comprobante_url = f"/uploads/comprobantes/recibo_{random.randint(1000, 9999)}.pdf"
        
        return self.pago_repo.guardar_pago(
            id_usuario=id_usuario,
            id_inmueble=data.id_inmueble,
            monto=data.monto,
            metodo_pago=data.metodo_pago,
            comprobante_url=comprobante_url
        )

    def obtener_historial_pagos(self, usuario_id: int, usuario_autenticado: dict) -> HistorialPagosResponse:
        
        id_usuario_auth = usuario_autenticado.get('id_usuario')
        id_rol_auth = usuario_autenticado.get('id_rol')
        
        if id_usuario_auth != usuario_id and id_rol_auth != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para consultar los pagos de otro usuario"
            )
        
        pagos = self.pago_repo.get_pagos_by_usuario(usuario_id)
        
        # Obtener información del inmueble para cada pago
        pagos_con_inmueble = []
        for pago in pagos:
            inmueble = self.inmueble_repo.get_by_id(pago.id_inmueble)
            inmueble_info = InmuebleInfo(
                id_inmueble=inmueble.id_inmueble,
                numero=inmueble.numero,
                torre=inmueble.torre
            )
            pagos_con_inmueble.append(
                PagoHistorialResponse(
                    id_pago=pago.id_pago,
                    inmueble=inmueble_info,
                    monto=pago.monto,
                    metodo_pago=pago.metodo_pago,
                    estado=pago.estado,
                    fecha_pago=pago.fecha_pago,
                    comprobante_url=pago.comprobante_url
                )
            )
        
        # TODO: Obtener datos reales del usuario desde un repositorio de usuarios
        usuario_info = UsuarioInfo(
            id_usuario=usuario_id,
            nombre_completo=f"Usuario {usuario_id}",
            email=f"usuario{usuario_id}@example.com"
        )
        
        return HistorialPagosResponse(
            usuario=usuario_info,
            pagos=pagos_con_inmueble
        )