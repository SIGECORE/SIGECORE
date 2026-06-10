# app/api/v1/router.py
from fastapi import APIRouter
from api.v1.usuarios import router as usuarios_router
from api.v1.inmuebles import router as inmuebles_router
from api.v1.pagos import router as pagos_router
#from api.v1.zonas import router as zonas_router
from api.v1.comunicados import router as comunicados_router
from api.v1.reportes import router as reportes_router

router = APIRouter()
router.include_router(usuarios_router)
router.include_router(inmuebles_router)
router.include_router(pagos_router)
#router.include_router(zonas_router)
router.include_router(comunicados_router)
router.include_router(reportes_router)