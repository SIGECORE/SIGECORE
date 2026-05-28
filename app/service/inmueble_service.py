# app/service/inmueble_service.py
from fastapi import HTTPException, status
from schemas import InmuebleCreate, InmuebleResponse, ListaInmueblesResponse, PaginacionInfo
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

        if self.repo.exists_by_numero_torre(data.numero, data.torre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un inmueble con el número {data.numero} en la torre {data.torre}"
            )

        return self.repo.create(data)

    def asignar_propietario(self, inmueble_id: int, id_propietario: int, usuario_autenticado: dict) -> InmuebleResponse:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Se requiere rol de administrador"
            )
        
        inmueble = self.repo.get_by_id(inmueble_id)
        if not inmueble:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inmueble con ID {inmueble_id} no encontrado"
            )
        
        if inmueble.id_propietario is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El inmueble ya tiene un propietario asignado"
            )
        
        return self.repo.asignar_propietario(inmueble_id, id_propietario, usuario_autenticado.get('id_usuario'))

    def listar_inmuebles(self, usuario_autenticado: dict, torre: str = None, 
                         estado: str = None, nombre_propietario: str = None,
                         page: int = 1, limit: int = 10) -> ListaInmueblesResponse:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Se requiere rol de administrador"
            )
        
        if estado and estado not in ["disponible", "ocupado", "mantenimiento"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado debe ser: disponible, ocupado o mantenimiento"
            )
        
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