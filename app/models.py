from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base


class UsuarioModel(Base):

    __tablename__ = "usuarios"

    id_usuario = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre_completo = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        nullable=False,
        unique=True
    )

    telefono = Column(
        String(20),
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    id_rol = Column(
        Integer,
        nullable=False
    )

    activo = Column(
        Boolean,
        default=True
    )

    fecha_registro = Column(
        DateTime,
        server_default=func.now()
    )

    intentos_fallidos = Column(
        Integer,
        default=0
    )

    bloqueado_hasta = Column(
        DateTime,
        nullable=True
    )

    ultimo_login = Column(
        DateTime,
        nullable=True
    )

    ip_registro = Column(
        String(45),
        nullable=True
    )

    user_agent = Column(
        String,
        nullable=True
    )