# app/repository/auditoria_repository.py
from typing import Dict, List
from domain.models_domain import AuditoriaRolResponse
from datetime import datetime


class AuditoriaRepository:

    def __init__(self):
        self._db: Dict[int, AuditoriaRolResponse] = {}
        self._next_id: int = 1

    def registrar_cambio_rol(self, id_usuario_modificado: int, rol_anterior: int, 
                              rol_nuevo: int, id_usuario_modificador: int, 
                              ip_origen: str = None) -> AuditoriaRolResponse:
        auditoria = AuditoriaRolResponse(
            id_auditoria=self._next_id,
            id_usuario_modificado=id_usuario_modificado,
            rol_anterior=rol_anterior,
            rol_nuevo=rol_nuevo,
            id_usuario_modificador=id_usuario_modificador,
            fecha_modificacion=datetime.now(),
            ip_origen=ip_origen
        )
        self._db[self._next_id] = auditoria
        self._next_id += 1
        return auditoria