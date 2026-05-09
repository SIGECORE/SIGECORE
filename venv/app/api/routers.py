from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

# Crear el router
router = APIRouter()

# Ruta de health check
@router.get("/health", response_model=dict)
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "environment": "development",
        "timestamp": datetime.now().isoformat()
    }

# Ruta principal
@router.get("/")
async def root():
    return {
        "mensaje": "Bienvenido a SIGECORE API",
        "documentacion": "/docs",
        "redoc": "/redoc"
    }

# Ejemplo de CRUD para usuarios
usuarios_db = []  # Simulación de base de datos

@router.get("/usuarios", response_model=List[dict])
async def get_usuarios():
    return usuarios_db

@router.post("/usuarios", status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario: dict):
    usuario["id"] = len(usuarios_db) + 1
    usuario["created_at"] = datetime.now().isoformat()
    usuarios_db.append(usuario)
    return {"mensaje": "Usuario creado", "usuario": usuario}

@router.get("/usuarios/{usuario_id}")
async def get_usuario(usuario_id: int):
    for usuario in usuarios_db:
        if usuario.get("id") == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")