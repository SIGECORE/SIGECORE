# repository/usuario_repository.py

from typing import Optional, List
from datetime import datetime
import bcrypt

from app.domain.models_domain import Usuario, UsuarioCreate


class UsuarioRepository:

    def __init__(self):
        self._db: dict[int, Usuario] = {}
        self._passwords: dict[int, str] = {}
        self._next_id: int = 1

    def existe_por_email(self, email: str) -> bool:
        email = email.lower()

        for usuario in self._db.values():
            if usuario.email.lower() == email:
                return True

        return False

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        email = email.lower()

        for usuario in self._db.values():
            if usuario.email.lower() == email:
                return usuario

        return None

    def listar(self) -> List[Usuario]:
        return list(self._db.values())

    def create(self, data: UsuarioCreate) -> Usuario:

        # Normalizar email
        email_normalizado = data.email.lower()

        # Encriptar contraseña con bcrypt
        password_hash = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt(rounds=10)
        ).decode("utf-8")

        # Obtener nombre del rol
        rol_nombre = (
            "administrador"
            if data.id_rol == 1
            else "residente"
        )

        usuario = Usuario(
            id_usuario=self._next_id,
            nombre_completo=data.nombre_completo,
            email=email_normalizado,
            telefono=data.telefono,
            id_rol=data.id_rol,
            rol_nombre=rol_nombre,
            activo=True,
            fecha_registro=datetime.now()
        )

        # Guardar usuario
        self._db[self._next_id] = usuario

        # Guardar hash de contraseña separado
        self._passwords[self._next_id] = password_hash

        self._next_id += 1

        return usuario

    def obtener_password_hash(self, id_usuario: int) -> Optional[str]:
        return self._passwords.get(id_usuario)