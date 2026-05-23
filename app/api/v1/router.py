from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/api/v1/zonas", status_code=201, tags=["Zonas Comunes"])
async def registrar_zona(
    request: dict,
    db: Session = Depends(get_db)
):
    return {
        "success": True,
        "statusCode": 201,
        "message": "Zona común registrada exitosamente"
    }