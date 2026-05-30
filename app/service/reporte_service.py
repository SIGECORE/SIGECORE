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
    
    def actualizar_estado(
    self,
    id_reporte,
    data,
    usuario_logueado,
    db,
    usuario_repository
):

        if usuario_logueado["id_rol"] != 1:

            raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "ACCESO_DENEGADO",
                    "details": "Se requiere rol de administrador para actualizar el estado de reportes",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

        reporte = self.repository.obtener_por_id(
        db,
        id_reporte
    )

        if not reporte:

            raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "statusCode": 404,
                "message": "Reporte no encontrado",
                "error": {
                    "error_code": "REPORTE_NOT_FOUND",
                    "details": f"No existe un reporte con el ID {id_reporte}",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

        if data.estado not in [
        "en_proceso",
        "resuelto"
    ]:

            raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ESTADO_INVALIDO",
                    "details": "El estado debe ser: en_proceso o resuelto",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

        if data.id_responsable:

            responsable = (
            usuario_repository.obtener_por_id(
                db,
                data.id_responsable
            )
        )

        if not responsable:

            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Responsable no encontrado",
                    "error": {
                        "error_code": "RESPONSABLE_NOT_FOUND",
                        "details": f"No existe un usuario con el ID {data.id_responsable}",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        reporte.responsable_id = (
            data.id_responsable
        )

        reporte.estado = data.estado

        reporte.observaciones = (
        data.observaciones
    )

        reporte.fecha_actualizacion = (
        datetime.utcnow()
    )

        if data.estado == "resuelto":

            reporte.fecha_resolucion = (
            datetime.utcnow()
        )

        self.repository.actualizar(
        db,
        reporte
    )

        return reporte