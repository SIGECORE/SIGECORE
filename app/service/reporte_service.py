from datetime import datetime

from fastapi import HTTPException


class ReporteService:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def crear_reporte(
        self,
        data,
        usuario
    ):

        tipos_validos = [
            "daño",
            "queja",
            "solicitud"
        ]

        if data.tipo not in tipos_validos:

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "TIPO_INVALIDO",
                        "details": "El tipo debe ser: daño, queja o solicitud",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        if not data.descripcion.strip():

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo descripcion es obligatorio",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        reporte = {
            "id_usuario": usuario["id_usuario"],
            "nombre_usuario": usuario["nombre_completo"],
            "tipo": data.tipo,
            "descripcion": data.descripcion,
            "evidencias": data.evidencias,
            "estado": "pendiente",
            "fecha_reporte": datetime.utcnow()
        }

        return self.repository.create(
            reporte
        )

    def listar_reportes(self):

        return self.repository.listar()

    def obtener_reporte(
        self,
        id_reporte: int
    ):

        return self.repository.obtener_por_id(
            id_reporte
        )

    def listar_por_usuario(
        self,
        id_usuario: int
    ):

        return self.repository.obtener_por_usuario(
            id_usuario
        )