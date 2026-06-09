# app/repositories.py
from repository.zona_repository import ZonaRepository
from repository.reserva_repository import ReservaRepository
from repository.usuario_repository import UsuarioRepository

# Instancias globales (compartidas por toda la aplicación)
zona_repo = ZonaRepository()
reserva_repo = ReservaRepository()
usuario_repo = UsuarioRepository()