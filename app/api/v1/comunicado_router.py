from datetime import datetime

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)

from fastapi.responses import JSONResponse

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

service = ComunicadoService(
    repo
)

router = APIRouter(
    prefix="/api/v1/comunicados",
    tags=["comunicados"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Publicar Comunicado"
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


@router.get(
    "/activos",
    status_code=status.HTTP_200_OK,
    summary="Consultar Comunicados Activos"
)
def consultar_comunicados_activos(
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

    usuario = validar_token(
        token
    )

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

    comunicados = (
        service.consultar_comunicados_activos(
            usuario
        )
    )

    if len(comunicados) == 0:

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "statusCode": 200,
                "message": "No hay comunicados activos en este momento",
                "data": {
                    "comunicados": []
                }
            }
        )

    resultado = []

    for comunicado in comunicados:

        resultado.append(
            {
                "id_comunicado": comunicado["id_comunicado"],
                "titulo": comunicado["titulo"],
                "contenido": comunicado["contenido"],
                "autor": {
                    "id_autor": comunicado["id_autor"],
                    "nombre": comunicado["autor_nombre"]
                },
                "archivos_adjuntos": comunicado[
                    "archivos_adjuntos"
                ],
                "fecha_publicacion": comunicado[
                    "fecha_publicacion"
                ].isoformat()
            }
        )

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Consulta exitosa",
            "data": {
                "comunicados": resultado
            }
        }
    )