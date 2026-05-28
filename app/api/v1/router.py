# api/v1/router.py
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.domain.models_domain import UsuarioLogin
from app.repository.usuario_repository import UsuarioRepository
from app.service.usuario_service import UsuarioService


repo = UsuarioRepository()
service = UsuarioService(repo)

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["usuarios"]
)


# ===== HISTORIA 2 DEPENDE DE HISTORIA 1 =====
# Login utiliza usuarios registrados previamente

@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
def login(
    data: UsuarioLogin
):

    resultado = service.login(data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Inicio de sesión exitoso",
            "data": resultado
        }
    )