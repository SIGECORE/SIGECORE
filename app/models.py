from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

# ==================== Modelos existentes (ajusta según lo que ya tenías) ====================

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    
    reservas = relationship("Reserva", back_populates="usuario")

# ==================== HU-008: Modelos para Disponibilidad ====================

class EstadoZonaEnum(str, enum.Enum):
    DISPONIBLE = "disponible"
    MANTENIMIENTO = "mantenimiento"

class EstadoReservaEnum(str, enum.Enum):
    APROBADA = "aprobada"
    PENDIENTE = "pendiente"
    CANCELADA = "cancelada"

class ZonaComun(Base):
    __tablename__ = "zonas_comunes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    capacidad = Column(Integer, nullable=True)
    estado = Column(SQLEnum(EstadoZonaEnum), default=EstadoZonaEnum.DISPONIBLE)
    
    reservas = relationship("Reserva", back_populates="zona")

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    zona_id = Column(Integer, ForeignKey("zonas_comunes.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(SQLEnum(EstadoReservaEnum), default=EstadoReservaEnum.PENDIENTE)
    
    zona = relationship("ZonaComun", back_populates="reservas")
    usuario = relationship("Usuario", back_populates="reservas")