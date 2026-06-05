from datetime import datetime


class UsuarioRepository:

    def __init__(self):

        self.usuarios = []

        self.next_id = 1

    def existe_por_email(
        self,
        email: str
    ):

        return any(
            usuario["email"] == email
            for usuario in self.usuarios
        )

    def obtener_por_email(
        self,
        email: str
    ):

        for usuario in self.usuarios:

            if usuario["email"] == email:

                return usuario

        return None

    def create(
        self,
        usuario: dict
    ):

        usuario["id_usuario"] = self.next_id

        self.next_id += 1

        self.usuarios.append(usuario)

        return usuario

    def actualizar(
        self,
        usuario_actualizado: dict
    ):

        for i, usuario in enumerate(self.usuarios):

            if (
                usuario["id_usuario"]
                == usuario_actualizado["id_usuario"]
            ):

                self.usuarios[i] = usuario_actualizado

                return usuario_actualizado

        return None