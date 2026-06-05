from datetime import datetime

from fastapi import HTTPException


class ComunicadoService:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def publicar_comunicado(
        self,
        data,
        usuario
    ):

        # Solo administradores
        if usuario["id_rol"] != 1:

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

        # Validar título
        if not data.titulo.strip():

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo titulo es obligatorio",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        # Validar contenido
        if not data.contenido.strip():

            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo contenido es obligatorio",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            )

        # Validar fecha de expiración
        if data.fecha_expiracion:

            fecha_exp = data.fecha_expiracion

            if fecha_exp.replace(
                tzinfo=None
            ) < datetime.utcnow():

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

        comunicado = {
            "titulo": data.titulo,
            "contenido": data.contenido,
            "id_autor": usuario["id_usuario"],
            "autor_nombre": usuario["nombre_completo"],
            "archivos_adjuntos": data.archivos_adjuntos,
            "fecha_publicacion": datetime.utcnow(),
            "fecha_expiracion": data.fecha_expiracion,
            "activo": True
        }

        return self.repository.create(
            comunicado
        )