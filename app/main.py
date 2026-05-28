from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.api.v1 import disponibilidad

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

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

# Registrar routers
app.include_router(disponibilidad.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "API de Zonas Comunes",
        "version": "1.0.0",
        "endpoints": {
            "disponibilidad": "/api/v1/zonas/disponibilidad"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}