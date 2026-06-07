# app/service/rol_service.py
from datetime import datetime
from fastapi import HTTPException, status
from domain.models_domain import AsignarRolRequest
from repository.usuario_repository import UsuarioRepository
from repository.auditoria_repository import AuditoriaRepository


class RolService:

    def __init__(self, usuario_repo: UsuarioRepository, auditoria_repo: AuditoriaRepository):
        self.usuario_repo = usuario_repo
        self.auditoria_repo = auditoria_repo

    def asignar_rol(self, usuario_id: int, data: AsignarRolRequest, usuario_autenticado: dict, client_ip: str = None):
        
        id_usuario_auth = usuario_autenticado.get('id_usuario')
        id_rol_auth = usuario_autenticado.get('id_rol')
        
        if id_rol_auth != 1:
            raise HTTPException(status_code=403, detail="Acceso denegado")
        
        if id_usuario_auth == usuario_id:
            raise HTTPException(status_code=400, detail="No puedes cambiar tu propio rol")
        
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        if data.id_rol not in [1, 2]:
            raise HTTPException(status_code=400, detail="Rol inválido")
        
        rol_anterior = usuario.id_rol
        usuario_actualizado = self.usuario_repo.update_rol(usuario_id, data.id_rol)
        
        self.auditoria_repo.registrar_cambio_rol(
            id_usuario_modificado=usuario_id,
            rol_anterior=rol_anterior,
            rol_nuevo=data.id_rol,
            id_usuario_modificador=id_usuario_auth,
            ip_origen=client_ip
        )
        
        return {"success": True, "message": "Rol actualizado"}