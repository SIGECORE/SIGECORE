# app/service/inmueble_service.py
from typing import Optional, List
from fastapi import HTTPException, status
from domain.models_domain import Inmueble, ListaInmueblesResponse, PaginacionInfo
from repository.inmueble_repository import InmuebleRepository


class InmuebleService:

    def __init__(self, repo: InmuebleRepository):
        self.repo = repo

    def listar_inmuebles(self, usuario_autenticado: dict, torre: Optional[str] = None, 
                         estado: Optional[str] = None, nombre_propietario: Optional[str] = None,
                         page: int = 1, limit: int = 10) -> ListaInmueblesResponse:
        
        # Validar permisos (solo administradores)
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Se requiere rol de administrador para consultar todos los inmuebles"
            )
        
        # Validar estado
        if estado and estado not in ["disponible", "ocupado", "mantenimiento"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado debe ser: disponible, ocupado o mantenimiento"
            )
        
        # Validar paginación
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:
            limit = 10
        
        inmuebles, total = self.repo.listar_con_filtros(torre, estado, nombre_propietario, page, limit)
        
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