from sqlalchemy.orm import Session
from app.models import ZonaComun  # Asumiendo que tienes el modelo SQLAlchemy

class ZonaRepository:
    def __init__(self, db: Session):
        self.db = db

    def existe_nombre(self, nombre: str) -> bool:
        return self.db.query(ZonaComun).filter(ZonaComun.nombre == nombre).first() is not None

    def crear(self, zona_data: dict) -> ZonaComun:
        nueva_zona = ZonaComun(**zona_data)
        self.db.add(nueva_zona)
        self.db.commit()
        self.db.refresh(nueva_zona)
        return nueva_zona