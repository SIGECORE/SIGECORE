# app/main.py
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from api.v1.router import router

app = FastAPI(
    title="SIGECORE API",
    description="API REST para gestión de conjuntos residenciales",
    version="1.0.0",
    swagger_ui_parameters={"persistAuthorization": True}
)

# Esto es necesario para que Swagger muestre el botón Authorize
security = HTTPBearer()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "¡API de SIGECORE funcionando! 🚀"}