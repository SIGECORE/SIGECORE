# app/service/comunicado_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import ComunicadoCreate, ComunicadoResponse
from repository.comunicado_repository import ComunicadoRepository


class ComunicadoService:

    def __init__(self, repo: ComunicadoRepository):
        self.repo = repo

    def publicar_comunicado(self, data: ComunicadoCreate, usuario_autenticado: dict) -> ComunicadoResponse:
        
        # Validar campos obligatorios
        if not data.titulo or not data.contenido:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "Los campos titulo y contenido son obligatorios",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar fecha de expiración (si se envía)
        if data.fecha_expiracion and data.fecha_expiracion < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "FECHA_EXPIRACION_INVALIDA",
                        "details": "La fecha de expiración no puede ser anterior a la fecha actual",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        id_autor = usuario_autenticado.get('id_usuario')
        autor_nombre = usuario_autenticado.get('nombre_completo', f"Usuario {id_autor}")
        
        return self.repo.create(data, id_autor, autor_nombre)

    def listar_comunicados_activos(self) -> list[ComunicadoResponse]:
        return self.repo.get_activos()