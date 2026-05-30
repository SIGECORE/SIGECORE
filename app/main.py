from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api.v1.zonas import router as zonas_router

# Inicializar base de datos
init_db()

# Crear aplicación
app = FastAPI(
    title="API de Zonas Comunes",
    description="API para gestión de zonas comunes",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(zonas_router)

@app.get("/")
def root():
    return {"message": "API de Zonas Comunes", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}