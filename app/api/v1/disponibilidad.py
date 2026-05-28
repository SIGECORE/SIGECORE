from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import date, time, datetime
from typing import Optional
from app.database import get_db
from app.service.disponibilidad_service import DisponibilidadService
from app.domain.disponibilidad_domain import DisponibilidadDomain, ErrorCode
from app.schemas import DisponibilidadResponse

router = APIRouter()

# Función de autenticación temporal (REEMPLAZAR con tu autenticación real)
async def get_current_user(token: Optional[str] = None):
    """
    Temporal: Reemplazar con tu implementación real de autenticación
    """
    # Simular usuario autenticado
    return {"id": 1, "nombre": "Usuario Test", "email": "test@test.com"}
    
    # Tu implementación real debería ser algo como:
    # if not token:
    #     raise HTTPException(status_code=401, detail="No autenticado")
    # user = verify_token(token)
    # return user

@router.get("/zonas/disponibilidad", response_model=DisponibilidadResponse)
async def consultar_disponibilidad(
    zona_id: Optional[int] = Query(None, description="ID de la zona común"),
    fecha: Optional[date] = Query(None, description="Fecha a consultar (YYYY-MM-DD)"),
    hora_inicio: Optional[time] = Query(None, description="Hora de inicio (HH:MM)"),
    hora_fin: Optional[time] = Query(None, description="Hora de fin (HH:MM)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Autenticación requerida
):
    """
    Consulta de disponibilidad de zonas comunes.
    
    - **zona_id**: ID de la zona común
    - **fecha**: Fecha a consultar (YYYY-MM-DD)
    - **hora_inicio**: Hora de inicio (HH:MM)
    - **hora_fin**: Hora de fin (HH:MM)
    """
    
    # Validar parámetros obligatorios
    error = DisponibilidadDomain.validar_parametros_obligatorios(zona_id, fecha, hora_inicio, hora_fin)
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
    error = DisponibilidadDomain.validar_fecha(fecha)
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
    error = DisponibilidadDomain.validar_horario(hora_inicio, hora_fin)
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
    
    # Verificar disponibilidad
    try:
        service = DisponibilidadService(db)
        disponibilidad_data = service.verificar_disponibilidad(
            zona_id, fecha, hora_inicio, hora_fin
        )
        
        if disponibilidad_data.disponible:
            return DisponibilidadResponse(
                success=True,
                statusCode=200,
                message="La zona está disponible",
                data=disponibilidad_data
            )
        else:
            return DisponibilidadResponse(
                success=True,
                statusCode=200,
                message="La zona no está disponible en el horario solicitado",
                data=disponibilidad_data
            )
            
    except Exception as e:
        if str(e) == ErrorCode.ZONA_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Zona no encontrada",
                    "error": {
                        "error_code": ErrorCode.ZONA_NOT_FOUND,
                        "details": f"No existe una zona común con el ID {zona_id}",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        elif str(e) == ErrorCode.ZONA_MANTENIMIENTO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Zona no disponible",
                    "error": {
                        "error_code": ErrorCode.ZONA_MANTENIMIENTO,
                        "details": "La zona común está actualmente en mantenimiento y no puede ser reservada",
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
                        "details": str(e),
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )