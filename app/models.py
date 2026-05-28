from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

# ==================== Enums ====================

class EstadoZonaEnum(str, enum.Enum):
    DISPONIBLE = "disponible"
    MANTENIMIENTO = "mantenimiento"

class EstadoReservaEnum(str, enum.Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    CANCELADA = "cancelada"

class RolEnum(str, enum.Enum):
    ADMINISTRADOR = "administrador"
    RESIDENTE = "residente"

# ==================== Modelo Usuario ====================

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    rol = Column(String(20), default=RolEnum.RESIDENTE)
    activo = Column(Boolean, default=True)
    tiene_morosidad = Column(Boolean, default=False)
    
    reservas = relationship("Reserva", foreign_keys="Reserva.usuario_id", back_populates="usuario")
    reservas_aprobadas = relationship("Reserva", foreign_keys="Reserva.aprobado_por", back_populates="aprobador")
    reservas_canceladas = relationship("Reserva", foreign_keys="Reserva.cancelado_por", back_populates="cancelador")

# ==================== Modelo ZonaComun ====================

class ZonaComun(Base):
    __tablename__ = "zonas_comunes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)
    capacidad = Column(Integer, nullable=True)
    estado = Column(String(20), default=EstadoZonaEnum.DISPONIBLE)
    
    reservas = relationship("Reserva", back_populates="zona")

# ==================== Modelo Reserva ====================

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    zona_id = Column(Integer, ForeignKey("zonas_comunes.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(String(20), default=EstadoReservaEnum.PENDIENTE)
    observaciones = Column(Text, nullable=True)
    fecha_solicitud = Column(DateTime, default=datetime.now)
    fecha_aprobacion = Column(DateTime, nullable=True)
    aprobado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_cancelacion = Column(DateTime, nullable=True)
    cancelado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    zona = relationship("ZonaComun", back_populates="reservas")
    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="reservas")
    aprobador = relationship("Usuario", foreign_keys=[aprobado_por], back_populates="reservas_aprobadas")
    cancelador = relationship("Usuario", foreign_keys=[cancelado_por], back_populates="reservas_canceladas")