# app/service/pago_service.py
import random
from fastapi import HTTPException, status
from datetime import datetime
from domain.models_domain import (
    PagoRequest, PagoResponse, HistorialPagosResponse,
    UsuarioInfo, PagoHistorialResponse, InmuebleInfo,
    ReporteCarteraResponse, InmuebleCartera, PropietarioCartera, ItemCartera
)
from repositories import pago_repo
from repositories import inmueble_repo
from repositories import usuario_repo


def procesar_pago_externo(monto: float, metodo_pago: str, token: str) -> bool:
    # Simula pasarela de pagos (80% éxito)
    return random.random() < 0.8


VALOR_CUOTA = 150000.00


class PagoService:

    def __init__(self, pago_repo, inmueble_repo, usuario_repo):
        self.pago_repo = pago_repo
        self.inmueble_repo = inmueble_repo
        self.usuario_repo = usuario_repo

    def registrar_pago(self, data: PagoRequest, usuario_autenticado: dict) -> PagoResponse:
        
        id_usuario = usuario_autenticado.get('id_usuario')
        id_rol = usuario_autenticado.get('id_rol')
        
        # Validar campos requeridos
        if not data.id_inmueble:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo id_inmueble es obligatorio",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        if not data.monto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo monto es obligatorio",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        if not data.metodo_pago:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo metodo_pago es obligatorio",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar monto
        if data.monto <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "MONTO_INVALIDO",
                        "details": "El monto debe ser mayor a 0",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que el inmueble existe
        inmueble = self.inmueble_repo.get_by_id(data.id_inmueble)
        if not inmueble:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Inmueble no encontrado",
                    "error": {
                        "error_code": "INMUEBLE_NOT_FOUND",
                        "details": f"No existe un inmueble con el ID {data.id_inmueble}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que el usuario es propietario o administrador
        es_propietario = (inmueble.id_propietario == id_usuario)
        es_admin = (id_rol == 1)
        
        if not es_propietario and not es_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "NO_AUTORIZADO",
                        "details": "No es propietario del inmueble asociado al pago",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Procesar pago con pasarela externa
        pago_exitoso = procesar_pago_externo(data.monto, data.metodo_pago, data.token_pasarela)
        
        if not pago_exitoso:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "success": False,
                    "statusCode": 502,
                    "message": "Error en el procesamiento del pago",
                    "error": {
                        "error_code": "PASARELA_ERROR",
                        "details": "La pasarela de pagos no está disponible en este momento",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Generar comprobante
        comprobante_url = f"/uploads/comprobantes/recibo_{random.randint(1000, 9999)}.pdf"
        
        # Guardar pago
        pago = self.pago_repo.guardar_pago(
            id_usuario=id_usuario,
            id_inmueble=data.id_inmueble,
            monto=data.monto,
            metodo_pago=data.metodo_pago,
            comprobante_url=comprobante_url
        )
        
        return pago

    def obtener_historial_pagos(self, usuario_id: int, usuario_autenticado: dict) -> HistorialPagosResponse:
        
        id_usuario_auth = usuario_autenticado.get('id_usuario')
        id_rol_auth = usuario_autenticado.get('id_rol')
        
        if id_usuario_auth != usuario_id and id_rol_auth != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "No tiene permisos para consultar los pagos de otro usuario",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        pagos = self.pago_repo.get_pagos_by_usuario(usuario_id)
        
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
        
        usuario = self.usuario_repo.get_by_id(usuario_id)
        usuario_info = UsuarioInfo(
            id_usuario=usuario.get("id_usuario"),
            nombre_completo=usuario.get("nombre_completo"),
            email=usuario.get("email")
        )
        
        return HistorialPagosResponse(
            usuario=usuario_info,
            pagos=pagos_con_inmueble
        )

    def generar_reporte_cartera(self, usuario_autenticado: dict, torre: str = None, meses_mora_min: int = None) -> dict:
        
        id_rol = usuario_autenticado.get('id_rol')
        
        if id_rol != 1:
            raise HTTPException(
                status_code=403,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador para generar el reporte de cartera",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        if meses_mora_min is not None and meses_mora_min <= 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "FILTRO_INVALIDO",
                        "details": "El parámetro meses_mora debe ser un número entero positivo",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Obtener todos los inmuebles
        todos_inmuebles = self.inmueble_repo.get_all_inmuebles()
        
        # Filtrar por torre si se especifica
        if torre:
            todos_inmuebles = [i for i in todos_inmuebles if i.torre == torre]
        
        # Filtrar solo inmuebles con propietario
        inmuebles_con_propietario = [i for i in todos_inmuebles if i.id_propietario is not None]
        
        fecha_actual = datetime.now()
        VALOR_CUOTA = 150000.00
        
        cartera = []
        total_adeudado_general = 0.0
        
        for inmueble in inmuebles_con_propietario:
            # Obtener el último pago del inmueble
            ultimo_pago = self.pago_repo.get_ultimo_pago_by_inmueble(inmueble.id_inmueble)
            
            if ultimo_pago:
                # Calcular meses desde el último pago
                meses_mora = (fecha_actual.year - ultimo_pago.fecha_pago.year) * 12 + (fecha_actual.month - ultimo_pago.fecha_pago.month)
                ultimo_pago_fecha = ultimo_pago.fecha_pago.strftime("%Y-%m-%d")
            else:
                # Si nunca ha pagado, la mora es desde la fecha de registro del inmueble
                meses_mora = (fecha_actual.year - inmueble.fecha_registro.year) * 12 + (fecha_actual.month - inmueble.fecha_registro.month)
                ultimo_pago_fecha = None
            
            # Si no hay mora o es negativa, no contar
            if meses_mora <= 0:
                continue
            
            # Aplicar filtro de meses_mora_min
            if meses_mora_min is not None and meses_mora < meses_mora_min:
                continue
            
            # Obtener datos del propietario
            propietario = self.usuario_repo.get_by_id(inmueble.id_propietario)
            if not propietario:
                continue
            
            total_adeudado = meses_mora * VALOR_CUOTA
            total_adeudado_general += total_adeudado
            
            cartera.append({
                "inmueble": {
                    "id_inmueble": inmueble.id_inmueble,
                    "numero": inmueble.numero,
                    "torre": inmueble.torre,
                    "area_m2": inmueble.area_m2
                },
                "propietario": {
                    "id_propietario": propietario.get("id_usuario"),
                    "nombre_completo": propietario.get("nombre_completo"),
                    "email": propietario.get("email"),
                    "telefono": propietario.get("telefono")
                },
                "meses_mora": meses_mora,
                "valor_cuota": VALOR_CUOTA,
                "total_adeudado": total_adeudado,
                "ultimo_pago": ultimo_pago_fecha
            })
        
        total_morosos = len(cartera)
        
        if total_morosos == 0:
            return {
                "success": True,
                "statusCode": 200,
                "message": "No hay residentes con pagos pendientes",
                "data": {
                    "fecha_generacion": datetime.now().isoformat(),
                    "total_morosos": 0,
                    "total_adeudado": 0,
                    "cartera": []
                }
            }
        
        return {
            "success": True,
            "statusCode": 200,
            "message": "Reporte generado exitosamente",
            "data": {
                "fecha_generacion": datetime.now().isoformat(),
                "total_morosos": total_morosos,
                "total_adeudado": total_adeudado_general,
                "cartera": cartera
            }
        }