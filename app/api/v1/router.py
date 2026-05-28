# api/v1/router.py
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.domain.models_domain import UsuarioLogin
from app.service.usuario_service import UsuarioService
from app.repository.usuario_repository import UsuarioRepository

repo = UsuarioRepository()
service = UsuarioService(repo)

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["usuarios"]
)

@router.post("/login")
def login(data: UsuarioLogin):

    resultado = service.login(data)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=resultado
    )