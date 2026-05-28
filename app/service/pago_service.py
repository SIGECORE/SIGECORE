# app/service/pago_service.py
from fastapi import HTTPException, status
from domain.models_domain import HistorialPagosResponse, UsuarioInfo
from repository.pago_repository import PagoRepository
from repository.usuario_repository import UsuarioRepository


class PagoService:

    def __init__(self, pago_repo: PagoRepository, usuario_repo: UsuarioRepository):
        self.pago_repo = pago_repo
        self.usuario_repo = usuario_repo

    def obtener_historial_pagos(self, usuario_id: int, usuario_autenticado: dict) -> HistorialPagosResponse:
        
        id_usuario_auth = usuario_autenticado.get('id_usuario')
        id_rol_auth = usuario_autenticado.get('id_rol')
        
        # Validar que el usuario existe
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un usuario con el ID {usuario_id}"
            )
        
        # Validar permisos (mismo usuario o administrador)
        es_mismo_usuario = (id_usuario_auth == usuario_id)
        es_admin = (id_rol_auth == 1)
        
        if not es_mismo_usuario and not es_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos para consultar los pagos de otro usuario"
            )
        
        # Obtener pagos del usuario
        pagos = self.pago_repo.get_pagos_by_usuario(usuario_id)
        
        return HistorialPagosResponse(
            usuario=UsuarioInfo(
                id_usuario=usuario.id_usuario,
                nombre_completo=usuario.nombre_completo,
                email=usuario.email
            ),
            pagos=pagos
        )