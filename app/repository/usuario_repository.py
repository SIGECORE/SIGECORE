<<<<<<< HEAD
# repository/usuario_repository.py

from typing import Optional, List
from datetime import datetime
import bcrypt

from domain.models_domain import Usuario, UsuarioCreate
=======
# app/repository/usuario_repository.py
from typing import Optional, Dict
from domain.models_domain import UsuarioResponse
from datetime import datetime
>>>>>>> 4a10eb2360e7de6d26d420d32c106822219cce6f


class UsuarioRepository:

    def __init__(self):
<<<<<<< HEAD
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
=======
        self._db: Dict[int, UsuarioResponse] = {}
        self._next_id: int = 1
        self._crear_usuarios_prueba()

    def _crear_usuarios_prueba(self):
        # Usuario administrador (ID 1)
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
        
        # Usuario residente (ID 2)
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
>>>>>>> 4a10eb2360e7de6d26d420d32c106822219cce6f
