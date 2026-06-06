# app/service/reporte_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import ReporteCreate, ReporteResponse, ActualizarReporteRequest
from repository.reporte_repository import ReporteRepository


class ReporteService:

    def __init__(self, repo: ReporteRepository):
        self.repo = repo

    def crear_reporte(self, data: ReporteCreate, usuario_autenticado: dict) -> ReporteResponse:
        
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

    def actualizar_estado(self, reporte_id: int, data: ActualizarReporteRequest, 
                          usuario_autenticado: dict) -> ReporteResponse:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        reporte = self.repo.get_by_id(reporte_id)
        if not reporte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Reporte no encontrado",
                    "error": {
                        "error_code": "REPORTE_NOT_FOUND",
                        "details": f"No existe un reporte con el ID {reporte_id}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        estados_validos = ["en_proceso", "resuelto"]
        if data.estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "ESTADO_INVALIDO",
                        "details": "El estado debe ser: en_proceso o resuelto",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        if reporte.estado == "resuelto" and data.estado != "resuelto":
            raise HTTPException(
                status_code=400,
                detail="No se puede modificar un reporte ya resuelto"
            )
        
        return self.repo.update_estado(
            reporte_id, data.estado, data.observaciones, data.id_responsable
        )