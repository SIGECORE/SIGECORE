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
        
        # Validar que sea administrador
        if id_rol_auth != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador para realizar esta acción",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que no se modifique a sí mismo
        if id_usuario_auth == usuario_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "AUTO_MODIFICACION_NO_PERMITIDA",
                        "details": "No puedes cambiar tu propio rol de administrador",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que el usuario existe
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Usuario no encontrado",
                    "error": {
                        "error_code": "USUARIO_NOT_FOUND",
                        "details": f"No existe un usuario con el ID {usuario_id}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        # Validar que el nuevo rol sea válido
        nuevo_rol = data.id_rol
        if nuevo_rol not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "ROL_INVALIDO",
                        "details": "El rol debe ser 1 (administrador) o 2 (residente)",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        rol_anterior = usuario.id_rol
        
        # Actualizar rol
        usuario_actualizado = self.usuario_repo.update_rol(usuario_id, nuevo_rol)
        
        # Registrar auditoría
        self.auditoria_repo.registrar_cambio_rol(
            id_usuario_modificado=usuario_id,
            rol_anterior=rol_anterior,
            rol_nuevo=nuevo_rol,
            id_usuario_modificador=id_usuario_auth,
            ip_origen=client_ip
        )
        
        rol_nombre = "administrador" if nuevo_rol == 1 else "residente"
        
        return {
            "success": True,
            "statusCode": 200,
            "message": "Rol actualizado exitosamente",
            "data": {
                "id_usuario": usuario_actualizado.id_usuario,
                "nombre_completo": usuario_actualizado.nombre_completo,
                "email": usuario_actualizado.email,
                "id_rol": nuevo_rol,
                "rol_nombre": rol_nombre,
                "actualizado_por": f"{usuario_autenticado.get('nombre_completo')} (ID: {id_usuario_auth})"
            }
        }