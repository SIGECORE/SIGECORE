from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import Optional
from app.service.zona_service import ZonaService
from app.domain.zona_domain import ErrorCode
from app.schemas import ZonaCreateRequest, ZonaResponse

router = APIRouter(tags=["Zonas Comunes"])

# Temporal - Reemplazar con autenticación real
async def get_current_user(token: Optional[str] = None):
    # Simular usuario administrador
    return {"id": 1, "nombre": "Administrador", "email": "admin@admin.com", "rol": "administrador"}

# ==================== POST /api/v1/zonas ====================
@router.post("/zonas", response_model=ZonaResponse, status_code=status.HTTP_201_CREATED)
async def registrar_zona(
    request: ZonaCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Registra una nueva zona común.
    
    **Campos obligatorios:**
    - **nombre**: Nombre de la zona común
    - **capacidad_maxima**: Capacidad máxima de personas
    
    **Reglas:**
    - Solo administradores pueden registrar zonas
    - El nombre debe ser único
    - La capacidad debe ser un número positivo
    - El estado inicial es "disponible"
    """
    
    try:
        service = ZonaService()
        zona = service.registrar_zona(
            nombre=request.nombre,
            capacidad_maxima=request.capacidad_maxima,
            descripcion=request.descripcion,
            horario_inicio=request.horario_inicio,
            horario_fin=request.horario_fin,
            usuario_actual=current_user
        )
        
        return ZonaResponse(
            success=True,
            statusCode=201,
            message="Zona común registrada exitosamente",
            data=zona
        )
        
    except Exception as e:
        error_str = str(e)
        
        if error_str == ErrorCode.NO_AUTENTICADO:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "statusCode": 401,
                    "message": "No autenticado",
                    "error": {
                        "error_code": ErrorCode.NO_AUTENTICADO,
                        "details": "Token de autenticación requerido",
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
                        "details": "Se requiere rol de administrador para registrar zonas",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        elif error_str == ErrorCode.ZONA_DUPLICADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": ErrorCode.ZONA_DUPLICADA,
                        "details": f"Ya existe una zona común con el nombre '{request.nombre}'",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        elif error_str == ErrorCode.CAPACIDAD_INVALIDA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": ErrorCode.CAPACIDAD_INVALIDA,
                        "details": "La capacidad máxima debe ser un número entero mayor a 0",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        elif error_str == ErrorCode.CAMPO_REQUERIDO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": ErrorCode.CAMPO_REQUERIDO,
                        "details": "Los campos 'nombre' y 'capacidad_maxima' son obligatorios",
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