from fastapi import FastAPI

from app.api.v1.router import router

from app.database import (
    Base,
    engine
)

from app.models import (
    UsuarioModel,
    ReporteModel
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SIGECORE API",
    description="API REST para la creacion de reportes en el sistema SIGECORE",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "¡API de SIGECORE funcionando! 🚀"
    }