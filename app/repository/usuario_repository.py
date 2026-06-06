<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> d3ef36a8e6d7c03bab413c6b442799cd76d7ae59
# app/repository/usuario_repository.py
from sqlalchemy.orm import Session
from models import Usuario as UsuarioModel


class UsuarioRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, usuario_id: int):
        return self.db.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()
<<<<<<< HEAD
    
    def get_by_email(self, email: str):
        return self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    
    def get_all(self):
        return self.db.query(UsuarioModel).all()
=======
=======
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
>>>>>>> 4141413e2aafba34c1f755d6873d474a052b4c43
>>>>>>> d3ef36a8e6d7c03bab413c6b442799cd76d7ae59
