from sqlalchemy.orm import Session

from app.models import ReporteModel


class ReporteRepository:

    def create(
        self,
        db: Session,
        reporte: ReporteModel
    ):

        db.add(reporte)

        db.commit()

        db.refresh(reporte)

        return reporte