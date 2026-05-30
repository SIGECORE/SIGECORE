from sqlalchemy.orm import Session

from app.models import ComunicadoModel


class ComunicadoRepository:

    def create(
        self,
        db: Session,
        comunicado: ComunicadoModel
    ):

        db.add(comunicado)

        db.commit()

        db.refresh(comunicado)

        return comunicado