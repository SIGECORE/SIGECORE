# app/service/inmueble_service.py
from fastapi import HTTPException, status
from domain.models_domain import Inmueble, InmuebleCreate
from repository.inmueble_repository import InmuebleRepository


# Simulación de base de datos de usuarios
USUARIOS_DB = {
    5: {"id_propietario": 5, "nombre_completo": "Carlos Rodríguez", "email": "carlos@example.com", "telefono": "3009876543", "activo": True},
}


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

        return self.repo.create(data)

    def asignar_propietario(self, inmueble_id: int, id_propietario: int, usuario_autenticado: dict) -> Inmueble:
        
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
        
        propietario = USUARIOS_DB.get(id_propietario)
        if not propietario or not propietario.get("activo"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un usuario activo con ID {id_propietario}"
            )
        
        return self.repo.asignar_propietario(
            inmueble_id, 
            id_propietario, 
            usuario_autenticado.get('id_usuario'),
            propietario
        )