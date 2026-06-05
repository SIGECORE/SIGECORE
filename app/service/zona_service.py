# app/service/zona_service.py
from fastapi import HTTPException, status
from domain.models_domain import ZonaCreate, ZonaResponse
from repository.zona_repository import ZonaRepository


class ZonaService:

    def __init__(self, repo: ZonaRepository):
        self.repo = repo

    def registrar_zona(self, data: ZonaCreate, usuario_autenticado: dict) -> ZonaResponse:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Se requiere rol de administrador"
            )

        if data.capacidad_maxima <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La capacidad máxima debe ser un número mayor a 0"
            )

        if self.repo.exists_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe una zona común con el nombre {data.nombre}"
            )

        return self.repo.create(data)