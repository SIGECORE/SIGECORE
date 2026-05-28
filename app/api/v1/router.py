from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.zona_service import ZonaService
from app.api.v1.zonas_schema import ZonaComunRequest
from datetime import datetime

router = APIRouter()

# Simulación de autenticación (cambiar después por tu middleware real)
def get_current_user():
    return {"rol_id": 1, "id_usuario": 1}

# ========== ENDPOINT HU-007 ==========
@router.post("/api/v1/zonas", status_code=201, tags=["Zonas Comunes"])
async def registrar_zona(
    request: ZonaComunRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ZonaService(db)
    result = service.registrar_zona(request.dict(), usuario_rol=current_user.get("rol_id"))
    
    if not result["success"]:
        raise HTTPException(status_code=result["statusCode"], detail=result)
    
    return result