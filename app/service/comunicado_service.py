from datetime import datetime

from fastapi import HTTPException

from app.models import ComunicadoModel


class ComunicadoService:

    def __init__(self, repository):
        self.repository = repository

    def publicar_comunicado(
        self,
        data,
        usuario_logueado,
        db
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
                        "details": "Se requiere rol de administrador para publicar comunicados",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        if (
            data.fecha_expiracion
            and data.fecha_expiracion < datetime.utcnow()
        ):

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "FECHA_EXPIRACION_INVALIDA",
                        "details": "La fecha de expiración no puede ser anterior a la fecha actual",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        comunicado = ComunicadoModel(
            titulo=data.titulo,
            contenido=data.contenido,
            id_autor=usuario_logueado["id_usuario"],
            archivos_adjuntos=",".join(
                data.archivos_adjuntos
            ),
            fecha_expiracion=data.fecha_expiracion,
            activo=True
        )

        comunicado = self.repository.create(
            db,
            comunicado
        )

        return comunicado
    
    def obtener_comunicados_activos(
    self,
    db
):

        comunicados = (
        self.repository
        .obtener_comunicados_activos(db)
    )

        return comunicados