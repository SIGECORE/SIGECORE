# app/service/reporte_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import ReporteCreate, ReporteResponse
from repository.reporte_repository import ReporteRepository


class ReporteService:

    def __init__(self, repo: ReporteRepository):
        self.repo = repo

    def crear_reporte(self, data: ReporteCreate, usuario_autenticado: dict) -> ReporteResponse:
        
        # Validar campos obligatorios
        if not data.tipo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo tipo es obligatorio",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        if not data.descripcion:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo descripcion es obligatorio",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar tipo
        tipos_validos = ["daño", "queja", "solicitud"]
        if data.tipo not in tipos_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "TIPO_INVALIDO",
                        "details": "El tipo debe ser: daño, queja o solicitud",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        id_usuario = usuario_autenticado.get('id_usuario')
        nombre_usuario = usuario_autenticado.get('nombre_completo', f"Usuario {id_usuario}")
        
        return self.repo.create(data, id_usuario, nombre_usuario)