from sqlalchemy import Column, Integer, String, Enum, Time, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class EstadoZonaEnum(enum.Enum):
    disponible = "disponible"
    mantenimiento = "mantenimiento"

class ZonaComun(Base):
    __tablename__ = "zonas_comunes"

    id_zona = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    capacidad_maxima = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(Enum(EstadoZonaEnum), default=EstadoZonaEnum.disponible)
    horario_inicio = Column(Time, nullable=True)
    horario_fin = Column(Time, nullable=True)
    fecha_registro = Column(DateTime, default=func.now())