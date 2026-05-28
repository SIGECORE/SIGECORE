from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.service.reserva_admin_service import ReservaAdminService
from app.domain.reserva_admin_domain import ReservaAdminDomain, ErrorCode
from app.schemas import ReservasPendientesResponse, CambioEstadoRequest, CambioEstadoResponse

router = APIRouter(tags=["Reservas"])

# Temporal - Reemplazar con autenticación real
async def get_current_user(token: Optional[str] = None):
    # Simular usuario administrador
    return {"id": 1, "nombre": "Admin Test", "email": "admin@test.com", "rol": "administrador"}

# ==================== GET /api/v1/reservas/pendientes ====================

@router.get("/reservas/pendientes", response_model=ReservasPendientesResponse)
async def listar_reservas_pendientes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todas las solicitudes de reserva pendientes.
    Requiere rol de administrador.
    """
    
    # Validar que sea administrador
    error = ReservaAdminDomain.validar_administrador(current_user)
    if error:
        status_code, error_code, error_detail = error
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "message": "Acceso denegado",
                "error": {
                    "error_code": error_code,
                    "details": error_detail["details"],
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )
    
    try:
        service = ReservaAdminService(db)
        reservas_pendientes = service.listar_reservas_pendientes()
        
        return ReservasPendientesResponse(
            success=True,
            statusCode=200,
            message="Consulta exitosa",
            data={"pendientes": reservas_pendientes}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "statusCode": 500,
                "message": "Error interno del servidor",
                "error": {
                    "error_code": "ERROR_INTERNO",
                    "details": str(e),
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )

# ==================== PATCH /api/v1/reservas/{id}/estado ====================

@router.patch("/reservas/{reserva_id}/estado", response_model=CambioEstadoResponse)
async def cambiar_estado_reserva(
    reserva_id: int,
    request: CambioEstadoRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Aprueba o rechaza una reserva pendiente.
    Requiere rol de administrador.
    
    - **estado**: "aprobada" o "rechazada"
    """
    
    # Validar que sea administrador
    error = ReservaAdminDomain.validar_administrador(current_user)
    if error:
        status_code, error_code, error_detail = error
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "message": "Acceso denegado",
                "error": {
                    "error_code": error_code,
                    "details": error_detail["details"],
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )
    
    # Validar estado válido
    error = ReservaAdminDomain.validar_estado_valido(request.estado)
    if error:
        status_code, error_code, error_detail = error
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "message": "Estado inválido",
                "error": {
                    "error_code": error_code,
                    "details": error_detail["details"],
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )
    
    try:
        service = ReservaAdminService(db)
        resultado = service.cambiar_estado_reserva(
            reserva_id=reserva_id,
            nuevo_estado=request.estado,
            administrador_id=current_user["id"]
        )
        
        mensaje = f"Reserva {request.estado} exitosamente"
        
        return CambioEstadoResponse(
            success=True,
            statusCode=200,
            message=mensaje,
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
        elif error_str == ErrorCode.RESERVA_NO_PENDIENTE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": ErrorCode.RESERVA_NO_PENDIENTE,
                        "details": "La reserva ya fue procesada anteriormente",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.RESERVA_CONFLICTO:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "success": False,
                    "statusCode": 409,
                    "message": "Conflicto de horario",
                    "error": {
                        "error_code": ErrorCode.RESERVA_CONFLICTO,
                        "details": "La zona ya está reservada en el horario solicitado",
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