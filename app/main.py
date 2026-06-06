# app/main.py
from fastapi import FastAPI
<<<<<<< HEAD
from api.v1.router import router
from database import engine
from models import Base

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIGECORE API",
    description="API REST para gestión de conjuntos residenciales",
    version="1.0.0"
)
=======
from fastapi.security import HTTPBearer
from api.v1.router import router

app = FastAPI(
    title="SIGECORE API",
    description="API REST para gestión de conjuntos residenciales",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

security = HTTPBearer()
>>>>>>> d3ef36a8e6d7c03bab413c6b442799cd76d7ae59

app.include_router(router)

@app.get("/")
def root():
<<<<<<< HEAD
    return {"message": "¡API de SIGECORE funcionando! 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
=======
    return {"message": "¡API de SIGECORE funcionando! 🚀"}
>>>>>>> d3ef36a8e6d7c03bab413c6b442799cd76d7ae59
