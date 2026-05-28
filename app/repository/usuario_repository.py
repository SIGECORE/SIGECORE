# repository/usuario_repository.py

from datetime import datetime
from typing import Optional

from app.domain.models_domain import Usuario


class UsuarioRepository:

    def __init__(self):
        self._db: dict[int, Usuario] = {}

    def buscar_por_email(
        self,
        email: str
    ) -> Optional[Usuario]:

        for usuario in self._db.values():
            if usuario.email == email.lower():
                return usuario

        return None

    def actualizar_intentos(
        self,
        usuario: Usuario,
        intentos: int
    ):

        usuario.intentos_fallidos = intentos

    def bloquear_usuario(
        self,
        usuario: Usuario,
        fecha_bloqueo: datetime
    ):

        usuario.bloqueado_hasta = fecha_bloqueo

    def resetear_intentos(
        self,
        usuario: Usuario
    ):

        usuario.intentos_fallidos = 0

    def actualizar_ultimo_login(
        self,
        usuario: Usuario
    ):

        usuario.ultimo_login = datetime.utcnow()