# app/api/v1/usuarios.py
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from domain.models_domain import AsignarRolRequest
from service.rol_service import RolService
from repository.usuario_repository import UsuarioRepository
from repository.auditoria_repository import AuditoriaRepository


SECRET_KEY = "mi_clave_secreta"
security = HTTPBearer()


def validar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {
            "id_usuario": payload.get("id_usuario"),
            "nombre_completo": payload.get("nombre_completo"),
            "email": payload.get("email"),
            "id_rol": payload.get("id_rol")
        }
    except:
        return None


router = APIRouter(tags=["Usuarios"])


@router.patch("/usuarios/{usuario_id}/rol")
def asignar_rol(
    usuario_id: int,
    data: AsignarRolRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    client_ip = request.client.host if request.client else None
    
    usuario_repo = UsuarioRepository()
    auditoria_repo = AuditoriaRepository()
    rol_service = RolService(usuario_repo, auditoria_repo)
    
    return rol_service.asignar_rol(usuario_id, data, usuario, client_ip)

@router.post("/public/crear-usuario-3")
def crear_usuario_3():
    from repositories import usuario_repo
    import bcrypt
    from datetime import datetime
    
    user_data = {
        'nombre_completo': 'Otro Residente',
        'email': 'otro@example.com',
        'telefono': '3001234567',
        'password_hash': bcrypt.hashpw('123456'.encode(), bcrypt.gensalt()).decode(),
        'id_rol': 2,
        'activo': True,
        'intentos_fallidos': 0,
        'bloqueado_hasta': None,
        'ultimo_login': None,
        'fecha_registro': datetime.now()
    }
    
    nuevo = usuario_repo.create(user_data)
    
    return {"message": "Usuario 3 creado", "id": nuevo["id_usuario"], "activo": nuevo["activo"]}