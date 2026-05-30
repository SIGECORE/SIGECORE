from sqlalchemy.orm import Session

from app.models import (
    UsuarioModel,
    AuditoriaRolesModel
)


class UsuarioRepository:

    def existe_por_email(
        self,
        db: Session,
        email: str
    ):

        return (
            db.query(UsuarioModel)
            .filter(
                UsuarioModel.email == email
            )
            .first()
            is not None
        )

    def obtener_por_email(
        self,
        db: Session,
        email: str
    ):

        return (
            db.query(UsuarioModel)
            .filter(
                UsuarioModel.email == email
            )
            .first()
        )

    def obtener_por_id(
        self,
        db: Session,
        id_usuario: int
    ):

        return (
            db.query(UsuarioModel)
            .filter(
                UsuarioModel.id_usuario == id_usuario
            )
            .first()
        )

    def create(
        self,
        db: Session,
        usuario: UsuarioModel
    ):

        db.add(usuario)

        db.commit()

        db.refresh(usuario)

        return usuario

    def actualizar(
        self,
        db: Session,
        usuario: UsuarioModel
    ):

        db.commit()

        db.refresh(usuario)

        return usuario

    def registrar_auditoria(
        self,
        db: Session,
        auditoria: AuditoriaRolesModel
    ):

        db.add(auditoria)

        db.commit()

        db.refresh(auditoria)

        return auditoria