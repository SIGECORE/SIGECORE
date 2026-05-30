from fastapi import FastAPI

from app.api.v1.router import router

from app.database import (
    Base,
    engine
)

from app.models import UsuarioModel

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIGECORE API",
    description="API REST para registro de usuarios en el sistema SIGECORE",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "¡API de SIGECORE funcionando! 🚀"
    }