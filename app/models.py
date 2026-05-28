# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from database import Base
import enum


class EstadoPago(str, enum.Enum):
    CONFIRMADO = "confirmado"
    RECHAZADO = "rechazado"
    PENDIENTE = "pendiente"


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
    estado = Column(String(20), default="disponible")
    id_propietario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())


class Pago(Base):
    __tablename__ = "pagos"

    id_pago = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_inmueble = Column(Integer, ForeignKey("inmuebles.id_inmueble"), nullable=False)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    estado = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE)
    comprobante_url = Column(String(255), nullable=True)
    referencia_externa = Column(String(100), nullable=True)
    fecha_pago = Column(DateTime(timezone=True), server_default=func.now())