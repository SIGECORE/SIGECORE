# app/api/v1/router.py (solo para HU-014)
from fastapi import APIRouter
from api.v1.comunicados import router as comunicados_router

router = APIRouter()
router.include_router(comunicados_router)