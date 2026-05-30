from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from typing import Optional
from app.service.zona_service import ZonaService
from app.domain.zona_domain import ErrorCode
from app.schemas import ZonaCreateRequest, ZonaUpdateRequest, ZonaResponse, ZonaListResponse

router = APIRouter(tags=["Zonas Comunes"])

# Temporal - Reemplazar con autenticación real
async def get_current_user(token: Optional[str] = None):
    return {"id": 1, "nombre": "Admin", "rol": "administrador"}

# ==================== GET /zonas ====================
@router.get("/zonas", response_model=ZonaListResponse)
async def listar_zonas(current_user: dict = Depends(get_current_user)):
    """Listar todas las zonas comunes"""
    try:
        service = ZonaService()
        zonas = service.listar_zonas()
        
        return ZonaListResponse(
            success=True,
            statusCode=200,
            message="Consulta exitosa",
            data=zonas
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
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

# ==================== GET /zonas/{id} ====================
@router.get("/zonas/{zona_id}", response_model=ZonaResponse)
async def obtener_zona(zona_id: int, current_user: dict = Depends(get_current_user)):
    """Obtener una zona por ID"""
    try:
        service = ZonaService()
        zona = service.obtener_zona(zona_id)
        
        if not zona:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Zona no encontrada",
                    "error": {
                        "error_code": ErrorCode.ZONA_NOT_FOUND,
                        "details": f"No existe una zona con el ID {zona_id}",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        return ZonaResponse(
            success=True,
            statusCode=200,
            message="Consulta exitosa",
            data=zona
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "statusCode": 500,
                "message": "Error interno",
                "error": {"error_code": "ERROR", "details": str(e)}
            }
        )

# ==================== POST /zonas ====================
@router.post("/zonas", response_model=ZonaResponse, status_code=201)
async def crear_zona(request: ZonaCreateRequest, current_user: dict = Depends(get_current_user)):
    """Crear una nueva zona común"""
    try:
        service = ZonaService()
        zona = service.crear_zona(request.nombre, request.descripcion, request.capacidad)
        
        return ZonaResponse(
            success=True,
            statusCode=201,
            message="Zona creada exitosamente",
            data=zona
        )
    except Exception as e:
        error_str = str(e)
        status_code = 400
        
        if error_str == ErrorCode.ZONA_NOMBRE_REQUERIDO:
            status_code = 400
        elif error_str == ErrorCode.ZONA_CAPACIDAD_INVALIDA:
            status_code = 400
        else:
            status_code = 500
        
        raise HTTPException(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "message": "Error al crear la zona",
                "error": {
                    "error_code": error_str,
                    "details": str(e),
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )

# ==================== PUT /zonas/{id} ====================
@router.put("/zonas/{zona_id}", response_model=ZonaResponse)
async def actualizar_zona(zona_id: int, request: ZonaUpdateRequest, current_user: dict = Depends(get_current_user)):
    """Actualizar una zona"""
    try:
        service = ZonaService()
        zona = service.actualizar_zona(
            zona_id, 
            request.nombre, 
            request.descripcion, 
            request.capacidad, 
            request.estado
        )
        
        return ZonaResponse(
            success=True,
            statusCode=200,
            message="Zona actualizada exitosamente",
            data=zona
        )
    except Exception as e:
        error_str = str(e)
        
        if error_str == ErrorCode.ZONA_NOT_FOUND:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Zona no encontrada",
                    "error": {
                        "error_code": ErrorCode.ZONA_NOT_FOUND,
                        "details": f"No existe una zona con el ID {zona_id}",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error al actualizar",
                "error": {
                    "error_code": error_str,
                    "details": str(e),
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )

# ==================== DELETE /zonas/{id} ====================
@router.delete("/zonas/{zona_id}", response_model=ZonaResponse)
async def eliminar_zona(zona_id: int, current_user: dict = Depends(get_current_user)):
    """Eliminar una zona"""
    try:
        service = ZonaService()
        service.eliminar_zona(zona_id)
        
        return ZonaResponse(
            success=True,
            statusCode=200,
            message="Zona eliminada exitosamente",
            data=None
        )
    except Exception as e:
        error_str = str(e)
        
        if error_str == ErrorCode.ZONA_NOT_FOUND:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Zona no encontrada",
                    "error": {
                        "error_code": ErrorCode.ZONA_NOT_FOUND,
                        "details": f"No existe una zona con el ID {zona_id}",
                        "timestamp": datetime.now().isoformat() + "Z"
                    }
                }
            )
        
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error al eliminar",
                "error": {
                    "error_code": error_str,
                    "details": str(e),
                    "timestamp": datetime.now().isoformat() + "Z"
                }
            }
        )