from fastapi import APIRouter
from api.v1.usuario_router import router as usuarios_router
from api.v1.inmuebles import router as inmuebles_router
from api.v1.pagos import router as pagos_router
from api.v1.zonas import router as zonas_router
from api.v1.comunicados import router as comunicados_router  # ← AGREGAR
from api.v1.reportes import router as reportes_router
from api.v1.reservas import router as reservas_router
from api.v1.reservas_aprobacion import router as reservas_aprobacion_router

router = APIRouter()
router.include_router(usuarios_router)
router.include_router(inmuebles_router)
router.include_router(pagos_router)
router.include_router(zonas_router)
router.include_router(comunicados_router)  # ← AGREGAR
router.include_router(reportes_router)
router.include_router(reservas_router)
router.include_router(reservas_aprobacion_router)