# app/repositories.py
from repository.usuario_repository import UsuarioRepository
from repository.zona_repository import ZonaRepository
from repository.reserva_repository import ReservaRepository
from repository.inmueble_repository import InmuebleRepository
from repository.pago_repository import PagoRepository
from repository.comunicado_repository import ComunicadoRepository
from repository.reporte_repository import ReporteRepository

# Instancias ÚNICAS (Singleton) - se crean una sola vez al iniciar la API
usuario_repo = UsuarioRepository()
zona_repo = ZonaRepository()
reserva_repo = ReservaRepository()
inmueble_repo = InmuebleRepository()
pago_repo = PagoRepository()
comunicado_repo = ComunicadoRepository()
reporte_repo = ReporteRepository()