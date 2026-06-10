# app/repository/usuario_repository.py
from typing import Optional, Dict, List
from datetime import datetime


class UsuarioRepository:

    def __init__(self):
        self._db: Dict[int, dict] = {}
        self._auditoria: List[dict] = []
        self._next_id: int = 1
        self._crear_usuarios_prueba()

    def _crear_usuarios_prueba(self):
        admin = {
            "id_usuario": 1,
            "nombre_completo": "Admin",
            "email": "admin@example.com",
            "telefono": "3000000000",
            "id_rol": 1,
            "activo": True,
            "fecha_registro": datetime.now(),
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
            "ultimo_login": None,
            "password_hash": "$2b$12$KIXq8ZuZkQZRqZqZqZqZquLmN5x7v8y9z0a1b2c3d4e5f6g7h8i9j0k"
        }
        self._db[1] = admin
        
        residente = {
            "id_usuario": 2,
            "nombre_completo": "María López",
            "email": "maria@example.com",
            "telefono": "3001234567",
            "id_rol": 2,
            "activo": True,
            "fecha_registro": datetime.now(),
            "intentos_fallidos": 0,
            "bloqueado_hasta": None,
            "ultimo_login": None,
            "password_hash": "$2b$12$KIXq8ZuZkQZRqZqZqZqZquLmN5x7v8y9z0a1b2c3d4e5f6g7h8i9j0k"
        }
        self._db[2] = residente
        self._next_id = 3

    def create(self, usuario_data: dict) -> dict:
        usuario_data["id_usuario"] = self._next_id
        usuario_data["activo"] = True  # ← FORZAR ACTIVO
        self._db[self._next_id] = usuario_data
        self._next_id += 1
        return usuario_data

    def get_by_id(self, usuario_id: int) -> Optional[dict]:
        return self._db.get(usuario_id)

    def get_by_email(self, email: str) -> Optional[dict]:
        for usuario in self._db.values():
            if usuario["email"].lower() == email.lower():
                return usuario
        return None

    def existe_por_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def obtener_por_email(self, email: str) -> Optional[dict]:
        return self.get_by_email(email)

    def obtener_por_id(self, usuario_id: int) -> Optional[dict]:
        return self.get_by_id(usuario_id)

    def actualizar(self, usuario_data: dict) -> dict:
        usuario_id = usuario_data.get("id_usuario")
        if usuario_id in self._db:
            self._db[usuario_id] = usuario_data
            return usuario_data
        return None

    def set_activo(self, usuario_id: int, activo: bool) -> bool:
        user = self._db.get(usuario_id)
        if user:
            user["activo"] = activo
            self._db[usuario_id] = user
            return True
        return False

    def get_all(self) -> Dict[int, dict]:
        return self._db

    def get_auditoria(self) -> List[dict]:
        return self._auditoria

    def registrar_auditoria(self, auditoria_data: dict) -> dict:
        self._auditoria.append(auditoria_data)
        print(f"AUDITORIA: {auditoria_data}")
        return auditoria_data

    def update_intentos(self, usuario_id: int, intentos: int, bloqueado_hasta: datetime = None):
        usuario = self._db.get(usuario_id)
        if usuario:
            usuario["intentos_fallidos"] = intentos
            if bloqueado_hasta:
                usuario["bloqueado_hasta"] = bloqueado_hasta
            self._db[usuario_id] = usuario

    def reset_intentos(self, usuario_id: int):
        usuario = self._db.get(usuario_id)
        if usuario:
            usuario["intentos_fallidos"] = 0
            usuario["bloqueado_hasta"] = None
            self._db[usuario_id] = usuario

    def update_ultimo_login(self, usuario_id: int):
        usuario = self._db.get(usuario_id)
        if usuario:
            usuario["ultimo_login"] = datetime.now()
            self._db[usuario_id] = usuario