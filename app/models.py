from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

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


class AuditoriaRolesModel(Base):

    __tablename__ = "auditoria_roles"

    id_auditoria = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_usuario_modificado = Column(
        Integer,
        nullable=False
    )

    rol_anterior = Column(
        Integer,
        nullable=False
    )

    rol_nuevo = Column(
        Integer,
        nullable=False
    )

    id_usuario_modificador = Column(
        Integer,
        nullable=False
    )

    fecha_modificacion = Column(
        DateTime,
        server_default=func.now()
    )

    ip_origen = Column(
        String(45),
        nullable=True
    )

    
class ComunicadoModel(Base):

    __tablename__ = "comunicados"

    id_comunicado = Column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo = Column(
        String(200),
        nullable=False
    )

    contenido = Column(
        String,
        nullable=False
    )

    id_autor = Column(
        Integer,
        nullable=False
    )

    archivos_adjuntos = Column(
        String,
        nullable=True
    )

    fecha_publicacion = Column(
        DateTime,
        server_default=func.now()
    )

    fecha_expiracion = Column(
        DateTime,
        nullable=True
    )

    activo = Column(
        Boolean,
        default=True
    )


class ReporteModel(Base):

    __tablename__ = "reportes"

    id_reporte = Column(
        Integer,
        primary_key=True,
        index=True
    )

    id_usuario = Column(
        Integer,
        nullable=False
    )

    tipo = Column(
        String(20),
        nullable=False
    )

    descripcion = Column(
        String,
        nullable=False
    )

    evidencias = Column(
        String,
        nullable=True
    )

    estado = Column(
        String(20),
        default="pendiente"
    )

    responsable_id = Column(
        Integer,
        nullable=True
    )

    fecha_reporte = Column(
        DateTime,
        server_default=func.now()
    )

    fecha_resolucion = Column(
        DateTime,
        nullable=True
    )