from typing import Tuple, Optional

class ErrorCode:
    NO_AUTENTICADO = "NO_AUTENTICADO"
    USUARIO_NOT_FOUND = "USUARIO_NOT_FOUND"
    ACCESO_DENEGADO = "ACCESO_DENEGADO"

class ConsultaDomain:
    
    @staticmethod
    def validar_acceso(usuario_autenticado_id, usuario_autenticado_rol, usuario_consultado_id) -> Optional[Tuple[int, str, dict]]:
        """Validar que el usuario autenticado sea el mismo o administrador"""
        if usuario_autenticado_rol != "administrador" and usuario_autenticado_id != usuario_consultado_id:
            return (403, ErrorCode.ACCESO_DENEGADO,
                   {"error_code": ErrorCode.ACCESO_DENEGADO,
                    "details": "No tiene permisos para consultar las reservas de otro usuario"})
        return None