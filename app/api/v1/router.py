from fastapi import APIRouter 
router = APIRouter() 
 
@router.post("/zonas") 
def crear_zona(): 
    return {"message": "ok"} 
# app/api/v1/router.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/zonas")
def crear_zona():
    return {"message": "Zona creada"}