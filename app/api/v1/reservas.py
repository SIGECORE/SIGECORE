from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.database import get_db
from app.service.reserva_service import ReservaService
from app.domain.reserva_domain import ReservaDomain, ErrorCode
from app.schemas import SolicitudReservaRequest, SolicitudReservaResponse

router = APIRouter(tags=["Reservas"])

# Temporal - Reemplazar con autenticación real
async def get_current_user(token: Optional[str] = None):
    return {"id": 1, "nombre": "Carlos Rodríguez", "email": "carlos@test.com", "activo": True, "tiene_morosidad": False}

@router.post("/reservas", response_model=SolicitudReservaResponse, status_code=status.HTTP_201_CREATED)
async def solicitar_reserva(
    request: SolicitudReservaRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Validar parámetros obligatorios
    error = ReservaDomain.validar_parametros_obligatorios(
        request.id_zona, request.fecha, request.hora_inicio, request.hora_fin
    )
    if error:
        status_code, error_code, error_detail = error
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "message": "Parámetro requerido faltante",
                "error": {
                    "error_code": error_code,
                    "details": error_detail["details"],
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )
    
    # Validar fecha
    error = ReservaDomain.validar_fecha(request.fecha)
    if error:
        status_code, error_code, error_detail = error
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "message": "Fecha inválida",
                "error": {
                    "error_code": error_code,
                    "details": error_detail["details"],
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )
    
    # Validar horario
    error = ReservaDomain.validar_horario(request.hora_inicio, request.hora_fin)
    if error:
        status_code, error_code, error_detail = error
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "message": "Horario inválido",
                "error": {
                    "error_code": error_code,
                    "details": error_detail["details"],
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )
    
    # Crear reserva
    try:
        service = ReservaService(db)
        reserva_data = service.crear_solicitud_reserva(
            usuario_id=current_user["id"],
            id_zona=request.id_zona,
            fecha=request.fecha,
            hora_inicio=request.hora_inicio,
            hora_fin=request.hora_fin,
            observaciones=request.observaciones
        )
        
        return SolicitudReservaResponse(
            success=True,
            statusCode=201,
            message="Solicitud de reserva creada exitosamente, pendiente de aprobación",
            data=reserva_data
        )
        
    except Exception as e:
        error_str = str(e)
        
        if error_str == ErrorCode.ZONA_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Zona no encontrada",
                    "error": {
                        "error_code": ErrorCode.ZONA_NOT_FOUND,
                        "details": f"No existe una zona común con el ID {request.id_zona}",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.ZONA_MANTENIMIENTO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Zona no disponible",
                    "error": {
                        "error_code": ErrorCode.ZONA_MANTENIMIENTO,
                        "details": "La zona común está actualmente en mantenimiento",
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
        elif error_str == ErrorCode.MOROSIDAD:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "No se puede realizar la reserva",
                    "error": {
                        "error_code": ErrorCode.MOROSIDAD,
                        "details": "El residente tiene pagos pendientes de cuotas de administración",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif error_str == ErrorCode.USUARIO_INACTIVO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Usuario inactivo",
                    "error": {
                        "error_code": ErrorCode.USUARIO_INACTIVO,
                        "details": "El usuario no está activo en el sistema",
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