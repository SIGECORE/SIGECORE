# app/repositories.py
from repository.reserva_repository import ReservaRepository
from repository.zona_repository import ZonaRepository
from repository.usuario_repository import UsuarioRepository

# Instancias globales (compartidas por toda la aplicación)
reserva_repo = ReservaRepository()
zona_repo = ZonaRepository()
usuario_repo = UsuarioRepository()