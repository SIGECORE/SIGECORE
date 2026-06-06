<<<<<<< HEAD
from datetime import datetime

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)
=======
# app/api/v1/router.py
from fastapi import APIRouter
from api.v1.usuarios import router as usuarios_router
from api.v1.inmuebles import router as inmuebles_router
from api.v1.pagos import router as pagos_router
from api.v1.zonas import router as zonas_router
>>>>>>> 4a10eb2360e7de6d26d420d32c106822219cce6f

router = APIRouter()

<<<<<<< HEAD
import jwt

from domain.models_domain import (
    ComunicadoCreate
)

from repository.comunicado_repository import (
    ComunicadoRepository
)

from service.comunicado_service import (
    ComunicadoService
)


SECRET_KEY = "mi_clave_secreta"


def validar_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return {
            "id_usuario": payload.get("id_usuario"),
            "nombre_completo": payload.get("nombre_completo"),
            "email": payload.get("email"),
            "id_rol": payload.get("id_rol")
        }

    except Exception:

        return None


repo = ComunicadoRepository()

service = ComunicadoService(repo)

router = APIRouter(
    prefix="/api/v1/comunicados",
    tags=["comunicados"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def publicar_comunicado(
    data: ComunicadoCreate,
    request: Request
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
                "message": "Usuario no autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Token requerido",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    token = (
        auth_header.split(" ")[1]
        if " " in auth_header
        else auth_header
    )

    usuario = validar_token(
        token
    )

    if not usuario:

        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "Usuario no autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Token inválido o expirado",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )

    comunicado = service.publicar_comunicado(
        data,
        usuario
    )

    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Comunicado publicado exitosamente",
            "data": {
                "id_comunicado": comunicado["id_comunicado"],
                "titulo": comunicado["titulo"],
                "contenido": comunicado["contenido"],
                "id_autor": comunicado["id_autor"],
                "autor_nombre": comunicado["autor_nombre"],
                "archivos_adjuntos": comunicado["archivos_adjuntos"],
                "fecha_publicacion": comunicado[
                    "fecha_publicacion"
                ].isoformat(),
                "fecha_expiracion": (
                    comunicado[
                        "fecha_expiracion"
                    ].isoformat()
                    if comunicado[
                        "fecha_expiracion"
                    ]
                    else None
                ),
                "activo": comunicado["activo"]
            }
        }
    )
=======
# Incluir todos los routers
router.include_router(usuarios_router)
router.include_router(inmuebles_router)
router.include_router(pagos_router)
router.include_router(zonas_router)
>>>>>>> 4a10eb2360e7de6d26d420d32c106822219cce6f
