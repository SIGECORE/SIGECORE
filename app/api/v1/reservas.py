from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.service.cancelacion_service import CancelacionService
from app.domain.cancelacion_domain import CancelacionDomain, ErrorCode
from app.schemas import CancelacionResponse

router = APIRouter(tags=["Reservas"])

# Temporal - Reemplazar con autenticación real
async def get_current_user(token: Optional[str] = None):
    # Simular usuario residente (cambiar a administrador para pruebas)
    return {"id": 1, "nombre": "Carlos Rodríguez", "email": "carlos@test.com", "rol": "residente"}

# ==================== DELETE /api/v1/reservas/{id} ====================

@router.delete("/reservas/{reserva_id}", response_model=CancelacionResponse)
async def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cancela una reserva existente.
    
    - Residentes: Solo pueden cancelar sus propias reservas con al menos 24 horas de anticipación
    - Administradores: Pueden cancelar cualquier reserva sin restricción de tiempo
    """
    
    try:
        service = CancelacionService(db)
        resultado = service.cancelar_reserva(
            reserva_id=reserva_id,
            usuario_id=current_user["id"],
            usuario_rol=current_user["rol"]
        )
        
        return CancelacionResponse(
            success=True,
            statusCode=200,
            message="Reserva cancelada exitosamente",
            data=resultado
        )
        
    except Exception as e:
        error_str = str(e)
        
        if error_str == ErrorCode.RESERVA_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Reserva no encontrada",
                    "error": {
                        "error_code": ErrorCode.RESERVA_NOT_FOUND,
                        "details": f"No existe una reserva con el ID {reserva_id}",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.NO_AUTORIZADO:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "No autorizado",
                    "error": {
                        "error_code": ErrorCode.NO_AUTORIZADO,
                        "details": "No tiene permiso para cancelar esta reserva",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.RESERVA_YA_CANCELADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": ErrorCode.RESERVA_YA_CANCELADA,
                        "details": "La reserva ya se encuentra cancelada",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.RESERVA_RECHAZADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": ErrorCode.RESERVA_RECHAZADA,
                        "details": "No se puede cancelar una reserva que ya fue rechazada",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.FECHA_PASADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "No se puede cancelar la reserva",
                    "error": {
                        "error_code": ErrorCode.FECHA_PASADA,
                        "details": "No se puede cancelar una reserva con fecha pasada",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.CANCELACION_TARDIA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "No se puede cancelar la reserva",
                    "error": {
                        "error_code": ErrorCode.CANCELACION_TARDIA,
                        "details": "Las reservas solo se pueden cancelar con al menos 24 horas de anticipación",
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