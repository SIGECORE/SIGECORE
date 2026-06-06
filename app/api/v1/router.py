# app/api/v1/router.py
from fastapi import APIRouter
from api.v1.usuarios import router as usuarios_router

router = APIRouter()
router.include_router(usuarios_router)