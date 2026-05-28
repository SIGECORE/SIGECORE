# main.py
from fastapi import FastAPI
from app.api.v1.router import router

app = FastAPI(
    title="SIGECORE API",
    description="API REST para registro de usuarios en el sistema SIGECORE",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {"message": "¡API de SIGECORE funcionando! 🚀"}