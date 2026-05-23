from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from service.zona_service import ZonaService
from api.v1.zonas_schema import ZonaComunRequest
from middleware.auth import verificar_token_y_rol
from datetime import datetime

router = APIRouter()

@router.post("/zonas", status_code=201)
async def registrar_zona(
    request: ZonaComunRequest,
    db: Session = Depends(get_db),
    payload: dict = Depends(verificar_token_y_rol)
):
    # Validar que el usuario sea administrador (rol_id = 1)
    if payload.get("rol_id") != 1:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "ACCESO_DENEGADO",
                    "details": "Solo los administradores pueden registrar zonas comunes",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        )

    service = ZonaService(db)
    result = service.registrar_zona(request.dict(), usuario_rol=payload.get("rol_id"))

    if not result["success"]:
        raise HTTPException(status_code=result["statusCode"], detail=result)

    return result