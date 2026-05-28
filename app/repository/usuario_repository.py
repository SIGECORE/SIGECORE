# repository/usuario_repository.py

from datetime import datetime
from app.domain.models_domain import Usuario


class UsuarioRepository:

    def __init__(self):

        # ===== DEPENDENCIA DE HU-001 =====
        # Usuarios registrados previamente
        self.usuarios = [

            Usuario(
                id_usuario=1,
                nombre_completo="Juan Pérez",
                email="juan@example.com",
                telefono="3001234567",
                id_rol=1,
                rol_nombre="administrador",
                activo=True,
                password_hash="$2b$12$3euPcmQFCiblsZeEu5s7p.KJ1y9Jt2Y7YQDdyCjTiMQuuLHfoalG2",
                intentos_fallidos=0,
                bloqueado_hasta=None,
                ultimo_login=None
            ),

            Usuario(
                id_usuario=2,
                nombre_completo="María López",
                email="maria@example.com",
                telefono="3019999999",
                id_rol=2,
                rol_nombre="residente",
                activo=True,
                password_hash="$2b$12$3euPcmQFCiblsZeEu5s7p.KJ1y9Jt2Y7YQDdyCjTiMQuuLHfoalG2",
                intentos_fallidos=0,
                bloqueado_hasta=None,
                ultimo_login=None
            )
        ]

    # ===== DEPENDENCIA HU-001 =====
    # Buscar usuario creado previamente
    def buscar_por_email(
        self,
        email: str
    ):

        for usuario in self.usuarios:

            if usuario.email.lower() == email.lower():
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
        bloqueo_hasta: datetime
    ):

        usuario.bloqueado_hasta = bloqueo_hasta

    def resetear_intentos(
        self,
        usuario: Usuario
    ):

        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta = None

    def actualizar_ultimo_login(
        self,
        usuario: Usuario
    ):

        usuario.ultimo_login = datetime.utcnow()