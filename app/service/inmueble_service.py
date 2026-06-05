# app/service/inmueble_service.py
from typing import Optional
from fastapi import HTTPException, status
from domain.models_domain import (
    InmuebleResponse, InmuebleCreate, ListaInmueblesResponse, PaginacionInfo
)
from repository.inmueble_repository import InmuebleRepository


class InmuebleService:

    def __init__(self, repo: InmuebleRepository):
        self.repo = repo

    def create_inmueble(self, data: InmuebleCreate, usuario_autenticado: dict) -> InmuebleResponse:
        
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

        return self.repo.create(data)

    def listar_inmuebles(self, torre: Optional[str] = None, estado: Optional[str] = None,
                         page: int = 1, limit: int = 10) -> ListaInmueblesResponse:
        
        if estado and estado not in ["disponible", "ocupado", "mantenimiento"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado debe ser: disponible, ocupado o mantenimiento"
            )
        
        inmuebles, total = self.repo.listar_con_filtros(torre, estado, page, limit)
        
        total_paginas = (total + limit - 1) // limit if total > 0 else 0
        
        return ListaInmueblesResponse(
            inmuebles=inmuebles,
            paginacion=PaginacionInfo(
                total=total,
                page=page,
                limit=limit,
                total_paginas=total_paginas
            )
        )