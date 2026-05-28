# app/service/pago_service.py
import random
from fastapi import HTTPException, status
from domain.models_domain import PagoRequest, PagoResponse
from repository.pago_repository import PagoRepository
from repository.inmueble_repository import InmuebleRepository


# Simulación de pasarela de pagos externa
def procesar_pago_externo(monto: float, metodo_pago: str, token: str) -> bool:
    # Simula éxito (80%) o fracaso (20%)
    return random.random() < 0.8


class PagoService:

    def __init__(self, pago_repo: PagoRepository, inmueble_repo: InmuebleRepository):
        self.pago_repo = pago_repo
        self.inmueble_repo = inmueble_repo

    def registrar_pago(self, data: PagoRequest, usuario_autenticado: dict) -> PagoResponse:
        
        id_usuario = usuario_autenticado.get('id_usuario')
        id_rol = usuario_autenticado.get('id_rol')
        
        # Validar autenticación
        if not id_usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticación requerido"
            )
        
        # Validar campos obligatorios
        if not data.id_inmueble:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo id_inmueble es obligatorio"
            )
        if not data.monto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo monto es obligatorio"
            )
        if not data.metodo_pago:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El campo metodo_pago es obligatorio"
            )
        
        # Validar monto
        if data.monto <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El monto debe ser mayor a 0"
            )
        
        # Validar que el inmueble existe
        inmueble = self.inmueble_repo.get_by_id(data.id_inmueble)
        if not inmueble:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un inmueble con el ID {data.id_inmueble}"
            )
        
        # Validar que el usuario sea propietario o administrador
        es_propietario = inmueble.id_propietario == id_usuario
        es_admin = (id_rol == 1)
        
        if not es_propietario and not es_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No es propietario del inmueble asociado al pago"
            )
        
        # Procesar pago con pasarela externa
        pago_exitoso = procesar_pago_externo(data.monto, data.metodo_pago, data.token_pasarela)
        
        if not pago_exitoso:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="La pasarela de pagos no está disponible en este momento"
            )
        
        # Generar comprobante (simulado)
        comprobante_url = f"/uploads/comprobantes/recibo_{random.randint(1000, 9999)}.pdf"
        
        # Guardar pago en repositorio
        pago = self.pago_repo.guardar_pago(
            id_usuario=id_usuario,
            id_inmueble=data.id_inmueble,
            monto=data.monto,
            metodo_pago=data.metodo_pago,
            comprobante_url=comprobante_url
        )
        
        return pago