from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from datetime import datetime

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Importar router de reservas
from app.api.v1.reservas import router as reservas_router

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Zonas Comunes",
    description="API para gestión de reservas de zonas comunes",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar router
app.include_router(reservas_router)

@app.get("/")
def read_root():
    return {
        "message": "API de Zonas Comunes",
        "version": "1.0.0",
        "endpoints": {
            "reservas_pendientes": "GET /api/v1/reservas/pendientes",
            "cambiar_estado": "PATCH /api/v1/reservas/{id}/estado",
            "docs": "GET /docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat() + "Z"}