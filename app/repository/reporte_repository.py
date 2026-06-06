from datetime import datetime

from domain.models_domain import Reporte


class ReporteRepository:

    def __init__(self):

        self._db: dict[int, Reporte] = {}

        self._next_id: int = 1

    def create(
        self,
        reporte: Reporte
    ):

        reporte.id_reporte = self._next_id

        self._db[self._next_id] = reporte

        self._next_id += 1

        return reporte

    def obtener_por_id(
        self,
        id_reporte: int
    ):

        return self._db.get(id_reporte)

    def listar(self):

        return list(
            self._db.values()
        )

    def actualizar(
        self,
        reporte: Reporte
    ):

        reporte.fecha_actualizacion = (
            datetime.utcnow()
        )

        self._db[
            reporte.id_reporte
        ] = reporte

        return reporte