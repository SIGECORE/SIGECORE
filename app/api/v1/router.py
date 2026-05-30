from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.zona_service import ZonaService
from app.schemas import ZonaComunCreate

router = APIRouter()

# Simulación de usuario autenticado (cambiar después por tu JWT)
def get_current_user():
    return {"rol_id": 1, "id_usuario": 1}

@router.post("/zonas", status_code=201, tags=["Zonas Comunes"])
def registrar_zona(
    zona_data: ZonaComunCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    service = ZonaService(db)
    result = service.registrar_zona(zona_data.dict(), usuario_rol=current_user.get("rol_id"))
    
    if not result["success"]:
        raise HTTPException(status_code=result["statusCode"], detail=result)
    
    return result