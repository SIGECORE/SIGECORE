# app/service/reporte_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import (
    ReporteCarteraResponse, ItemCartera, InmuebleCartera, PropietarioCartera
)
from repository.inmueble_repository import InmuebleRepository
from repository.pago_repository import PagoRepository


VALOR_CUOTA = 150000.00


class ReporteService:

    def __init__(self, inmueble_repo: InmuebleRepository, pago_repo: PagoRepository):
        self.inmueble_repo = inmueble_repo
        self.pago_repo = pago_repo

    def generar_reporte_cartera(self, usuario_autenticado: dict, torre: str = None, meses_mora_min: int = None) -> ReporteCarteraResponse:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Se requiere rol de administrador para generar el reporte de cartera"
            )
        
        if meses_mora_min is not None and meses_mora_min <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El parámetro meses_mora debe ser un número entero positivo"
            )
        
        inmuebles = self.inmueble_repo.get_all_inmuebles()
        
        if torre:
            inmuebles = [i for i in inmuebles if i.torre == torre]
        
        cartera = []
        total_adeudado = 0
        
        for inmueble in inmuebles:
            ultimo_pago = self.pago_repo.get_ultimo_pago_by_inmueble(inmueble.id_inmueble)
            
            if not inmueble.id_propietario:
                continue
            
            if ultimo_pago:
                meses_mora = 3  # Simulado
                ultimo_pago_str = ultimo_pago.fecha_pago.strftime("%Y-%m-%d")
            else:
                meses_mora = 4  # Simulado
                ultimo_pago_str = None
            
            if meses_mora_min is not None and meses_mora < meses_mora_min:
                continue
            
            if meses_mora > 0:
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
                        id_propietario=inmueble.id_propietario,
                        nombre_completo=f"Propietario {inmueble.id_propietario}",
                        email=f"propietario{inmueble.id_propietario}@example.com",
                        telefono="3000000000"
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