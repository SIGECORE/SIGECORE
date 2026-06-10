# app/repository/usuario_repository.py
from typing import Optional, Dict
from domain.models_domain import UsuarioResponse
from datetime import datetime


class UsuarioRepository:

    def __init__(self):
        self._db: Dict[int, UsuarioResponse] = {}
        self._next_id: int = 1
        self._crear_usuarios_prueba()

    def _crear_usuarios_prueba(self):
        admin = UsuarioResponse(
            id_usuario=1,
            nombre_completo="Admin",
            email="admin@example.com",
            telefono="3000000000",
            id_rol=1,
            activo=1,
            fecha_registro=datetime.now(),
            intentos_fallidos=0,
            bloqueado_hasta=None,
            ultimo_login=None
        )
        self._db[1] = admin
        
        residente = UsuarioResponse(
            id_usuario=2,
            nombre_completo="María López",
            email="maria@example.com",
            telefono="3001234567",
            id_rol=2,
            activo=1,
            fecha_registro=datetime.now(),
            intentos_fallidos=0,
            bloqueado_hasta=None,
            ultimo_login=None
        )
        self._db[2] = residente
        self._next_id = 3

    def get_by_id(self, usuario_id: int) -> Optional[UsuarioResponse]:
        return self._db.get(usuario_id)

    def get_by_email(self, email: str) -> Optional[UsuarioResponse]:
        for usuario in self._db.values():
            if usuario.email.lower() == email.lower():
                return usuario
        return None

    def update_rol(self, usuario_id: int, nuevo_rol: int) -> Optional[UsuarioResponse]:
        usuario = self._db.get(usuario_id)
        if not usuario:
            return None
        usuario.id_rol = nuevo_rol
        return usuario