from datetime import datetime


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

    def listar_activos(self):

        ahora = datetime.utcnow()

        comunicados_activos = []

        for comunicado in self._comunicados.values():

            # Debe estar activo
            if not comunicado["activo"]:
                continue

            fecha_expiracion = comunicado.get(
                "fecha_expiracion"
            )

            # Si tiene fecha de expiración y ya expiró
            if (
                fecha_expiracion is not None
                and fecha_expiracion.replace(
                    tzinfo=None
                ) <= ahora
            ):
                continue

            comunicados_activos.append(
                comunicado
            )

        # Ordenar por fecha_publicacion DESC
        comunicados_activos.sort(
            key=lambda x: x["fecha_publicacion"],
            reverse=True
        )

        return comunicados_activos