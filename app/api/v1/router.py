from datetime import datetime

import jwt

from fastapi import (
    APIRouter,
    Request,
    Depends,
    HTTPException,
    status
)

from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.database import get_db

from app.domain.models_domain import (
    ComunicadoCreate
)

from app.repository.comunicado_repository import (
    ComunicadoRepository
)

from app.service.comunicado_service import (
    ComunicadoService
)

SECRET_KEY = "mi_clave_secreta"

router = APIRouter(
    prefix="/api/v1/comunicados",
    tags=["comunicados"]
)


def validar_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except:

        return None


repo = ComunicadoRepository()

service = ComunicadoService(repo)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def publicar_comunicado(
    data: ComunicadoCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:

        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    token = (
        auth_header.split(" ")[1]
        if " " in auth_header
        else auth_header
    )

    usuario = validar_token(token)

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    comunicado = service.publicar_comunicado(
        data,
        usuario,
        db
    )

    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Comunicado publicado exitosamente",
            "data": {
                "id_comunicado": comunicado.id_comunicado,
                "titulo": comunicado.titulo,
                "contenido": comunicado.contenido,
                "id_autor": comunicado.id_autor,
                "autor_nombre": usuario["nombre_completo"],
                "archivos_adjuntos": (
                    comunicado.archivos_adjuntos.split(",")
                    if comunicado.archivos_adjuntos
                    else []
                ),
                "fecha_publicacion": comunicado.fecha_publicacion.isoformat(),
                "fecha_expiracion": (
                    comunicado.fecha_expiracion.isoformat()
                    if comunicado.fecha_expiracion
                    else None
                ),
                "activo": comunicado.activo
            }
        }
    )