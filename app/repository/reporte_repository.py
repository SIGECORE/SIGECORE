from sqlalchemy.orm import Session

from app.models import ReporteModel, UsuarioModel


class ReporteRepository:

    def create(
        self,
        db,
        reporte
    ):
        db.add(reporte)
        db.commit()
        db.refresh(reporte)
        return reporte

    def obtener_por_id(
        self,
        db,
        id_reporte
    ):
        return (
            db.query(ReporteModel)
            .filter(
                ReporteModel.id_reporte == id_reporte
            )
            .first()
        )

    def actualizar(
        self,
        db,
        reporte
    ):
        db.commit()
        db.refresh(reporte)
        return reporte
    
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