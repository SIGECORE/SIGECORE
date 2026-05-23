# main.py
from fastapi import FastAPI
from api.v1.router import router

app = FastAPI(
    title="SIGECORE API",
    description="API REST para gestión de conjuntos residenciales",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "¡API de SIGECORE funcionando! 🚀"}