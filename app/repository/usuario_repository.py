from sqlalchemy.orm import Session

from app.models import UsuarioModel


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

    def create(
        self,
        db: Session,
        usuario: UsuarioModel
    ):

        db.add(usuario)

        db.commit()

        db.refresh(usuario)

        return usuario
    
    def obtener_por_id(
    self,
    db,
    id_usuario
):
       return (
        db.query(UsuarioModel)
        .filter(
            UsuarioModel.id_usuario == id_usuario
        )
        .first()
    )