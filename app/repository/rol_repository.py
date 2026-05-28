# repository/rol_repository.py

from datetime import datetime

from app.domain.models_domain import (
    Usuario,
    AuditoriaRol
)


class RolRepository:

    def __init__(self):

        self._db: dict[int, Usuario] = {}
        self._auditoria: list[AuditoriaRol] = []
        self._next_auditoria_id = 1

    def buscar_usuario_por_id(
        self,
        id_usuario: int
    ):

        return self._db.get(id_usuario)

    def actualizar_rol(
        self,
        usuario: Usuario,
        nuevo_rol: int
    ):

        usuario.id_rol = nuevo_rol

        if nuevo_rol == 1:
            usuario.rol_nombre = "administrador"
        else:
            usuario.rol_nombre = "residente"

        return usuario

    def registrar_auditoria(
        self,
        id_usuario_modificado: int,
        rol_anterior: int,
        rol_nuevo: int,
        id_usuario_modificador: int,
        ip_origen: str | None
    ):

        auditoria = AuditoriaRol(
            id_auditoria=self._next_auditoria_id,
            id_usuario_modificado=id_usuario_modificado,
            rol_anterior=rol_anterior,
            rol_nuevo=rol_nuevo,
            id_usuario_modificador=id_usuario_modificador,
            fecha_modificacion=datetime.utcnow(),
            ip_origen=ip_origen
        )

        self._auditoria.append(auditoria)

        self._next_auditoria_id += 1