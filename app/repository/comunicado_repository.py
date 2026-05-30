from sqlalchemy.orm import Session

from app.models import ComunicadoModel
from datetime import datetime
from sqlalchemy import or_


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
    

def obtener_comunicados_activos(
    self,
    db
):

    return (
        db.query(ComunicadoModel)
        .filter(
            ComunicadoModel.activo == True,
            or_(
                ComunicadoModel.fecha_expiracion == None,
                ComunicadoModel.fecha_expiracion > datetime.utcnow()
            )
        )
        .order_by(
            ComunicadoModel.fecha_publicacion.desc()
        )
        .all()
    )