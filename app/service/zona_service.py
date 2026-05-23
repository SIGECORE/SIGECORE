from sqlalchemy.orm import Session
from app.repository.zona_repository import ZonaRepository
from app.domain.models_domain import ZonaComunDomain
from datetime import datetime

class ZonaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ZonaRepository(db)

    def registrar_zona(self, zona_data: dict, usuario_rol: int) -> dict:
        # Validación de administrador
        if usuario_rol != 1:
            return {
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "ACCESO_DENEGADO",
                    "details": "Solo los administradores pueden registrar zonas comunes",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }

        # Validar nombre único
        if self.repo.existe_nombre(zona_data["nombre"]):
            return {
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ZONA_DUPLICADA",
                    "details": f"Ya existe una zona común con el nombre '{zona_data['nombre']}'",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }

        # Crear zona
        nueva_zona = ZonaComunDomain(
            nombre=zona_data["nombre"],
            capacidad_maxima=zona_data["capacidad_maxima"],
            descripcion=zona_data.get("descripcion"),
            estado="disponible",
            horario_inicio=zona_data.get("horario_inicio"),
            horario_fin=zona_data.get("horario_fin"),
            fecha_registro=datetime.utcnow()
        )

        zona_creada = self.repo.crear(nueva_zona.dict(exclude_none=True))

        return {
            "success": True,
            "statusCode": 201,
            "message": "Zona común registrada exitosamente",
            "data": {
                "id_zona": zona_creada.id_zona,
                "nombre": zona_creada.nombre,
                "capacidad_maxima": zona_creada.capacidad_maxima,
                "descripcion": zona_creada.descripcion,
                "estado": zona_creada.estado.value if hasattr(zona_creada.estado, 'value') else zona_creada.estado,
                "horario_inicio": zona_creada.horario_inicio.isoformat() if zona_creada.horario_inicio else None,
                "horario_fin": zona_creada.horario_fin.isoformat() if zona_creada.horario_fin else None,
                "fecha_registro": zona_creada.fecha_registro.isoformat() + "Z"
            }
        }