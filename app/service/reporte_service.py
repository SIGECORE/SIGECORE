# app/service/reporte_service.py
from fastapi import HTTPException, status
from datetime import datetime
from dateutil.relativedelta import relativedelta
from domain.models_domain import (
    ReporteCarteraResponse, ItemCartera, InmuebleCartera, PropietarioCartera
)
from repository.inmueble_repository import InmuebleRepository
from repository.pago_repository import PagoRepository
from repository.usuario_repository import UsuarioRepository


# Valor de la cuota de administración (configurable)
VALOR_CUOTA = 150000.00


class ReporteService:

    def __init__(self, inmueble_repo: InmuebleRepository, pago_repo: PagoRepository, usuario_repo: UsuarioRepository):
        self.inmueble_repo = inmueble_repo
        self.pago_repo = pago_repo
        self.usuario_repo = usuario_repo

    def generar_reporte_cartera(self, usuario_autenticado: dict, torre: str = None, meses_mora_min: int = None) -> ReporteCarteraResponse:
        
        # Validar que sea administrador
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Se requiere rol de administrador para generar el reporte de cartera"
            )
        
        # Validar filtro meses_mora
        if meses_mora_min is not None and meses_mora_min <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El parámetro meses_mora debe ser un número entero positivo"
            )
        
        # Obtener inmuebles (con filtro de torre)
        if torre:
            inmuebles = self.inmueble_repo.get_by_torre(torre)
        else:
            inmuebles = self.inmueble_repo.get_all_inmuebles()
        
        cartera = []
        total_adeudado = 0
        
        for inmueble in inmuebles:
            # Obtener último pago
            ultimo_pago = self.pago_repo.get_ultimo_pago_by_inmueble(inmueble.id_inmueble)
            
            # Obtener propietario
            propietario = None
            if inmueble.id_propietario:
                propietario = self.usuario_repo.get_by_id(inmueble.id_propietario)
            
            # Calcular meses de mora
            if ultimo_pago:
                meses_mora = relativedelta(datetime.now(), ultimo_pago.fecha_pago).months
                ultimo_pago_str = ultimo_pago.fecha_pago.strftime("%Y-%m-%d")
            else:
                meses_mora = relativedelta(datetime.now(), inmueble.fecha_registro).months
                ultimo_pago_str = None
            
            # Filtrar por meses_mora mínimos
            if meses_mora_min is not None and meses_mora < meses_mora_min:
                continue
            
            # Solo mostrar morosos (meses_mora > 0)
            if meses_mora > 0 and propietario:
                deuda = meses_mora * VALOR_CUOTA
                total_adeudado += deuda
                
                cartera.append(ItemCartera(
                    inmueble=InmuebleCartera(
                        id_inmueble=inmueble.id_inmueble,
                        numero=inmueble.numero,
                        torre=inmueble.torre,
                        area_m2=inmueble.area_m2
                    ),
                    propietario=PropietarioCartera(
                        id_propietario=propietario.id_usuario,
                        nombre_completo=propietario.nombre_completo,
                        email=propietario.email,
                        telefono=propietario.telefono
                    ),
                    meses_mora=meses_mora,
                    valor_cuota=VALOR_CUOTA,
                    total_adeudado=deuda,
                    ultimo_pago=ultimo_pago_str
                ))
        
        return ReporteCarteraResponse(
            fecha_generacion=datetime.now(),
            total_morosos=len(cartera),
            total_adeudado=total_adeudado,
            cartera=cartera
        )