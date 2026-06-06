from datetime import datetime

from fastapi import HTTPException


class ReporteService:

    def __init__(
        self,
        reporte_repository,
        usuario_repository
    ):

        self.reporte_repository = reporte_repository
        self.usuario_repository = usuario_repository

    def actualizar_estado(
        self,
        id_reporte: int,
        data,
        usuario_logueado
    ):

        # Validar administrador
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

        # Buscar reporte
        reporte = self.reporte_repository.obtener_por_id(
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

        # Validar flujo de estados
        if reporte.estado == "pendiente":

            if data.estado != "en_proceso":

                raise HTTPException(
                    status_code=400,
                    detail={
                        "success": False,
                        "statusCode": 400,
                        "message": "Error en la solicitud",
                        "error": {
                            "error_code": "ESTADO_INVALIDO",
                            "details": "El flujo permitido es pendiente → en_proceso → resuelto",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    }
                )

        elif reporte.estado == "en_proceso":

            if data.estado != "resuelto":

                raise HTTPException(
                    status_code=400,
                    detail={
                        "success": False,
                        "statusCode": 400,
                        "message": "Error en la solicitud",
                        "error": {
                            "error_code": "ESTADO_INVALIDO",
                            "details": "El flujo permitido es pendiente → en_proceso → resuelto",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    }
                )

        elif reporte.estado == "resuelto":

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "ESTADO_INVALIDO",
                        "details": "No se puede modificar un reporte resuelto",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        responsable = None

        # Validar responsable
        if data.id_responsable is not None:

            responsable = (
                self.usuario_repository.obtener_por_id(
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
                            "details": f"No existe un usuario con ID {data.id_responsable}",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    }
                )

            reporte.id_responsable = (
                responsable.id_usuario
            )

        # Actualizar datos
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

        self.reporte_repository.actualizar(
            reporte
        )

        return {
            "id_reporte": reporte.id_reporte,
            "estado": reporte.estado,
            "observaciones": reporte.observaciones,
            "responsable": (
                {
                    "id_responsable": responsable.id_usuario,
                    "nombre": responsable.nombre_completo
                }
                if responsable
                else None
            ),
            "fecha_actualizacion": (
                reporte.fecha_actualizacion.isoformat()
            ),
            "fecha_resolucion": (
                reporte.fecha_resolucion.isoformat()
                if reporte.fecha_resolucion
                else None
            )
        }