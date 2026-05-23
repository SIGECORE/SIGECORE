from fastapi import FastAPI
from api.v1.router import router as zonas_router

app = FastAPI(title="SIGECORE API", version="0.1.0")

# Registrar rutas de zonas comunes
app.include_router(zonas_router)

@app.get("/")
def root():
    return {"message": "SIGECORE API"}

@app.get("/health")
def health():
    return {"status": "ok"}