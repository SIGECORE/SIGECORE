# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum


class EstadoInmueble(str, enum.Enum):
    DISPONIBLE = "disponible"
    OCUPADO = "ocupado"
    MANTENIMIENTO = "mantenimiento"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    id_rol = Column(Integer, nullable=False)
    activo = Column(Integer, default=1)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())


class Inmueble(Base):
    __tablename__ = "inmuebles"

    id_inmueble = Column(Integer, primary_key=True, index=True)
    numero = Column(String(10), nullable=False)
    torre = Column(String(10), nullable=False)
    area_m2 = Column(Float, nullable=False)
    estado = Column(Enum(EstadoInmueble), default=EstadoInmueble.DISPONIBLE)
    id_propietario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())


class AuditoriaInmueble(Base):
    __tablename__ = "auditoria_inmuebles"

    id_auditoria = Column(Integer, primary_key=True, index=True)
    id_inmueble = Column(Integer, ForeignKey("inmuebles.id_inmueble"), nullable=False)
    id_propietario_anterior = Column(Integer, nullable=True)
    id_propietario_nuevo = Column(Integer, nullable=False)
    id_usuario_modificador = Column(Integer, nullable=False)
    fecha_modificacion = Column(DateTime(timezone=True), server_default=func.now())