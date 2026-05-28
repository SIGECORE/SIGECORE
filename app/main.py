# app/main.py
from fastapi import FastAPI
from api.v1.router import router
from database import engine
from models import Base

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIGECORE API",
    description="API REST para gestión de conjuntos residenciales",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "¡API de SIGECORE funcionando! 🚀"}