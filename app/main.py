from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.api.v1.router import router

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIGECORE API", version="0.1.0")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "SIGECORE API"}

@app.get("/health")
def health():
    return {"status": "ok"}