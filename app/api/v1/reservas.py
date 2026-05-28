from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.service.consulta_service import ConsultaService
from app.domain.consulta_domain import ConsultaDomain, ErrorCode
from app.schemas import ConsultaReservasResponse

router = APIRouter(tags=["Reservas"])

# Temporal - Reemplazar con autenticación real
async def get_current_user(token: Optional[str] = None):
    # Simular usuario residente (cambiar a administrador para pruebas)
    return {"id": 1, "nombre": "Carlos Rodríguez", "email": "carlos@test.com", "rol": "residente"}

# ==================== GET /api/v1/reservas/usuario/{id} ====================

@router.get("/reservas/usuario/{usuario_id}", response_model=ConsultaReservasResponse)
async def consultar_reservas_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Consulta el historial completo de reservas de un usuario.
    
    - Residentes: Solo pueden consultar sus propias reservas
    - Administradores: Pueden consultar las reservas de cualquier usuario
    - Los resultados se ordenan por fecha descendente (más recientes primero)
    """
    
    try:
        service = ConsultaService(db)
        resultado = service.consultar_reservas_usuario(
            usuario_consultado_id=usuario_id,
            usuario_autenticado_id=current_user["id"],
            usuario_autenticado_rol=current_user["rol"]
        )
        
        # Verificar si tiene reservas
        if not resultado["reservas"]:
            return ConsultaReservasResponse(
                success=True,
                statusCode=200,
                message="El usuario no tiene reservas registradas",
                data=resultado
            )
        
        return ConsultaReservasResponse(
            success=True,
            statusCode=200,
            message="Consulta exitosa",
            data=resultado
        )
        
    except Exception as e:
        error_str = str(e)
        
        if error_str == ErrorCode.USUARIO_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Usuario no encontrado",
                    "error": {
                        "error_code": ErrorCode.USUARIO_NOT_FOUND,
                        "details": f"No existe un usuario con el ID {usuario_id}",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.ACCESO_DENEGADO:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": ErrorCode.ACCESO_DENEGADO,
                        "details": "No tiene permisos para consultar las reservas de otro usuario",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "success": False,
                    "statusCode": 500,
                    "message": "Error interno del servidor",
                    "error": {
                        "error_code": "ERROR_INTERNO",
                        "details": error_str,
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )