class ReporteRepository:

    def __init__(self):

        self._reportes = {}

        self._next_id = 1

    def create(
        self,
        reporte: dict
    ):

        reporte["id_reporte"] = self._next_id

        self._reportes[
            self._next_id
        ] = reporte

        self._next_id += 1

        return reporte

    def listar(self):

        return list(
            self._reportes.values()
        )

    def obtener_por_id(
        self,
        id_reporte: int
    ):

        return self._reportes.get(
            id_reporte
        )

    def obtener_por_usuario(
        self,
        id_usuario: int
    ):

        return [

            reporte

            for reporte in self._reportes.values()

            if reporte["id_usuario"] == id_usuario

        ]

    def actualizar_estado(
        self,
        id_reporte: int,
        estado: str
    ):

        reporte = self.obtener_por_id(
            id_reporte
        )

        if not reporte:

            return None

        reporte["estado"] = estado

        return reporte