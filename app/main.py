# app/main.py
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from api.v1.usuarios import router

app = FastAPI(
    title="SIGECORE API",
    description="API REST para gestión de conjuntos residenciales",
    version="1.0.0"
)

security = HTTPBearer()

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "¡API de SIGECORE funcionando! 🚀"}