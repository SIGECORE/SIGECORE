# app/service/inmueble_service.py
from fastapi import HTTPException, status
from domain.models_domain import InmuebleCreate, Inmueble
from repository.inmueble_repository import InmuebleRepository


class InmuebleService:

    def __init__(self, repo: InmuebleRepository):
        self.repo = repo

    def create_inmueble(self, data: InmuebleCreate, usuario_autenticado: dict) -> Inmueble:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Se requiere rol de administrador"
            )

        if data.area_m2 <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El área debe ser un número mayor a 0"
            )

        if self.repo.exists_by_numero_torre(data.numero, data.torre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un inmueble con el número {data.numero} en la torre {data.torre}"
            )

        return self.repo.create(data)