from sqlalchemy.orm import Session
from app.models import ZonaComun
from datetime import datetime

class ZonaService:
    def __init__(self, db: Session):
        self.db = db
    
    def registrar_zona(self, data: dict, usuario_rol: int):
        # Validar permisos de administrador
        if usuario_rol != 1:
            return {
                "success": False,
                "statusCode": 403,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ACCESO_DENEGADO",
                    "details": "No tiene permisos para registrar zonas comunes. Se requiere rol de administrador.",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        
        # Validar nombre duplicado
        zona_existente = self.db.query(ZonaComun).filter(ZonaComun.nombre == data["nombre"]).first()
        if zona_existente:
            return {
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ZONA_DUPLICADA",
                    "details": f"Ya existe una zona común con el nombre '{data['nombre']}'",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }
        
        try:
            zona = ZonaComun(
                nombre=data["nombre"],
                capacidad_maxima=data["capacidad_maxima"],
                descripcion=data.get("descripcion"),
                estado="disponible",
                horario_inicio=data.get("horario_inicio"),
                horario_fin=data.get("horario_fin"),
                fecha_registro=datetime.utcnow()
            )
            
            self.db.add(zona)
            self.db.commit()
            self.db.refresh(zona)
            
            horario_inicio = str(zona.horario_inicio)[:5] if zona.horario_inicio else None
            horario_fin = str(zona.horario_fin)[:5] if zona.horario_fin else None
            
            return {
                "success": True,
                "statusCode": 201,
                "message": "Zona común registrada exitosamente",
                "data": {
                    "id_zona": zona.id_zona,
                    "nombre": zona.nombre,
                    "capacidad_maxima": zona.capacidad_maxima,
                    "descripcion": zona.descripcion,
                    "estado": zona.estado,
                    "horario_inicio": horario_inicio,
                    "horario_fin": horario_fin,
                    "fecha_registro": zona.fecha_registro.isoformat() + "Z"
                }
            }
        except Exception as e:
            return {
                "success": False,
                "statusCode": 500,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ERROR_INTERNO",
                    "details": str(e),
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            }