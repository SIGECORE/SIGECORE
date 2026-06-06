# app/api/v1/usuarios.py
from fastapi import APIRouter
from domain.models_domain import LoginRequest
from service.auth_service import AuthService
from repository.usuario_repository import UsuarioRepository

router = APIRouter(tags=["Usuarios"])


@router.post("/usuarios/login")
def login(login_data: LoginRequest):
    usuario_repo = UsuarioRepository()
    auth_service = AuthService(usuario_repo)
    return auth_service.login(login_data)