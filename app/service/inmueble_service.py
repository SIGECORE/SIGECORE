# app/service/inmueble_service.py
from fastapi import HTTPException, status
from datetime import datetime
from domain.models_domain import (
    InmuebleResponse, InmuebleCreate, ListaInmueblesResponse,
    PaginacionInfo, InmuebleConPropietario
)
from repository.inmueble_repository import InmuebleRepository
from repositories import usuario_repo  # ← USAR EL REPOSITORIO CENTRAL


class InmuebleService:

    def __init__(self, repo: InmuebleRepository):
        self.repo = repo

    def create_inmueble(self, data: InmuebleCreate, usuario_autenticado: dict) -> InmuebleResponse:
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador para registrar inmuebles",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        if not data.numero:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo numero es obligatorio",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        if not data.torre:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "CAMPO_REQUERIDO",
                        "details": "El campo torre es obligatorio",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        if data.area_m2 <= 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "AREA_INVALIDA",
                        "details": "El área debe ser un número mayor a 0",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        if self.repo.exists_by_numero_torre(data.numero, data.torre):
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "INMUEBLE_DUPLICADO",
                        "details": f"Ya existe un inmueble con el número {data.numero} en la torre {data.torre}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        return self.repo.create(data)

    def listar_inmuebles(self, torre=None, estado=None, nombre_propietario=None, page=1, limit=10):
        
        if estado and estado not in ["disponible", "ocupado", "mantenimiento"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "ESTADO_INVALIDO",
                        "details": "El estado debe ser: disponible, ocupado o mantenimiento",
                        "timestamp": datetime.now().isoformat()
                    }
                }
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

    def asignar_propietario(self, inmueble_id: int, id_propietario: int, usuario_autenticado: dict):
        
        if usuario_autenticado.get('id_rol') != 1:
            raise HTTPException(
                status_code=403,
                detail={
                    "success": False,
                    "statusCode": 403,
                    "message": "Acceso denegado",
                    "error": {
                        "error_code": "ACCESO_DENEGADO",
                        "details": "Se requiere rol de administrador para asignar propietarios",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        inmueble = self.repo.get_by_id(inmueble_id)
        if not inmueble:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Inmueble no encontrado",
                    "error": {
                        "error_code": "INMUEBLE_NOT_FOUND",
                        "details": f"No existe un inmueble con el ID {inmueble_id}",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        if inmueble.id_propietario is not None:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "INMUEBLE_OCUPADO",
                        "details": "El inmueble ya tiene un propietario asignado",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        propietario = usuario_repo.get_by_id(id_propietario)
        
        if not propietario or not propietario.get("activo"):
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "statusCode": 404,
                    "message": "Propietario no encontrado",
                    "error": {
                        "error_code": "PROPIETARIO_NOT_FOUND",
                        "details": f"No existe un usuario con el ID {id_propietario} o el usuario está inactivo",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )
        
        return self.repo.asignar_propietario(inmueble_id, id_propietario)