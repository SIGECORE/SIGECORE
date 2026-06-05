# app/service/inmueble_service.py
from fastapi import HTTPException, status
from domain.models_domain import (
    InmuebleResponse, InmuebleCreate, ListaInmueblesResponse,
    PaginacionInfo, InmuebleConPropietario
)
from repository.inmueble_repository import InmuebleRepository


class InmuebleService:

    def __init__(self, repo: InmuebleRepository):
        self.repo = repo

    # ==================== HU-004 (Registro de inmuebles) ====================
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

    # ==================== HU-006 (Consulta de inmuebles) ====================
    def listar_inmuebles(self, torre=None, estado=None, nombre_propietario=None, page=1, limit=10):
        
        if estado and estado not in ["disponible", "ocupado", "mantenimiento"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado debe ser: disponible, ocupado o mantenimiento"
            )
        
        inmuebles, total = self.repo.listar_con_filtros(torre, estado, nombre_propietario, page, limit)
        
        total_paginas = (total + limit - 1) // limit if total > 0 else 0
        
        inmuebles_con_propietario = []
        for inmueble in inmuebles:
            inmuebles_con_propietario.append(
                InmuebleConPropietario(**inmueble.dict())
            )
        
        return ListaInmueblesResponse(
            inmuebles=inmuebles_con_propietario,
            paginacion=PaginacionInfo(
                total=total,
                page=page,
                limit=limit,
                total_paginas=total_paginas
            )
        )

    # ==================== HU-005 (Asignación de propietario) ====================
    def asignar_propietario(self, inmueble_id: int, id_propietario: int, usuario_autenticado: dict):
        
        # Verificar que el inmueble existe
        inmueble = self.repo.get_by_id(inmueble_id)
        if not inmueble:
            raise HTTPException(status_code=404, detail=f"Inmueble con ID {inmueble_id} no encontrado")
        
        # Verificar que no tenga ya un propietario
        if inmueble.id_propietario is not None:
            raise HTTPException(status_code=400, detail="El inmueble ya tiene un propietario asignado")
        
        # TODO: Validar que el usuario (id_propietario) existe en la tabla de usuarios
        # Por ahora simulamos que existe
        
        return self.repo.asignar_propietario(inmueble_id, id_propietario)