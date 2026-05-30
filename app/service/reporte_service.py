from datetime import datetime

from app.models import ReporteModel

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
        usuario,
        db
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

        reporte = ReporteModel(
            id_usuario=usuario["id_usuario"],
            tipo=data.tipo,
            descripcion=data.descripcion,
            evidencias=",".join(
                data.evidencias
            ),
            estado="pendiente"
        )

        return self.repository.create(
            db,
            reporte
        )