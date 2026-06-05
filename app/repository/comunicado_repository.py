class ComunicadoRepository:

    def __init__(self):

        self._comunicados = {}

        self._next_id = 1

    def create(
        self,
        comunicado: dict
    ):

        comunicado["id_comunicado"] = self._next_id

        self._comunicados[
            self._next_id
        ] = comunicado

        self._next_id += 1

        return comunicado

    def obtener_por_id(
        self,
        id_comunicado: int
    ):

        return self._comunicados.get(
            id_comunicado
        )

    def listar(self):

        return list(
            self._comunicados.values()
        )