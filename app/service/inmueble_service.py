# service/inmueble_service.py
from typing import List
from fastapi import HTTPException, status

from domain.models_domain import Inmueble, InmuebleCreate
from repository.inmueble_repository import InmuebleRepository


class InmuebleService:

    def __init__(self, repo: InmuebleRepository):
        self.repo = repo

    def get_all_inmuebles(self) -> List[Inmueble]:
        return self.repo.get_all()

    def get_inmueble(self, inmueble_id: int) -> Inmueble:
        inmueble = self.repo.get_by_id(inmueble_id)

        if not inmueble:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inmueble con ID {inmueble_id} no encontrado"
            )
        return inmueble

    def create_inmueble(self, data: InmuebleCreate, usuario_autenticado: dict) -> Inmueble:

        # Solo administradores (id_rol = 1)
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Se requiere rol de administrador"
            )

        # Área debe ser mayor a 0
        if data.area_m2 <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El área debe ser un número mayor a 0"
            )

        # No duplicado (mismo número y torre)
        if self.repo.existe_por_numero_y_torre(data.numero, data.torre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un inmueble con el número {data.numero} en la torre {data.torre}"
            )

        return self.repo.create(data)

    def delete_inmueble(self, inmueble_id: int) -> dict:
        deleted = self.repo.delete(inmueble_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inmueble con ID {inmueble_id} no encontrado"
            )
        return {"message": "Inmueble eliminado correctamente"}