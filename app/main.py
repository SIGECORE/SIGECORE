from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.api.v1.router import router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIGECORE API", version="1.0.0")

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "SIGECORE API - Registro de Zonas Comunes"}

@app.get("/health")
def health():
    return {"status": "ok"}