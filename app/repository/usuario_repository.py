# app/repository/usuario_repository.py
from typing import Optional, Dict
from domain.models_domain import UsuarioResponse
from datetime import datetime


class UsuarioRepository:

    def __init__(self):
        self._db: Dict[int, UsuarioResponse] = {}
        self._next_id: int = 1

    def create_default_user(self):
        """Crear un usuario de prueba para poder hacer login"""
        usuario = UsuarioResponse(
            id_usuario=self._next_id,
            nombre_completo="Juan Pérez",
            email="juan@example.com",
            telefono="3001234567",
            id_rol=2,
            activo=1,
            fecha_registro=datetime.now(),
            intentos_fallidos=0,
            bloqueado_hasta=None,
            ultimo_login=None
        )
        self._db[self._next_id] = usuario
        self._next_id += 1
        return usuario

    def get_by_email(self, email: str) -> Optional[UsuarioResponse]:
        for usuario in self._db.values():
            if usuario.email.lower() == email.lower():
                return usuario
        return None

    def update_intentos(self, usuario_id: int, intentos: int, bloqueado_hasta: datetime = None):
        usuario = self._db.get(usuario_id)
        if usuario:
            usuario.intentos_fallidos = intentos
            if bloqueado_hasta:
                usuario.bloqueado_hasta = bloqueado_hasta

    def reset_intentos(self, usuario_id: int):
        usuario = self._db.get(usuario_id)
        if usuario:
            usuario.intentos_fallidos = 0
            usuario.bloqueado_hasta = None
            usuario.ultimo_login = datetime.now()

    def update_ultimo_login(self, usuario_id: int):
        usuario = self._db.get(usuario_id)
        if usuario:
            usuario.ultimo_login = datetime.now()