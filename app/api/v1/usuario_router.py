from datetime import datetime

from fastapi import (
    APIRouter,
    status,
    Request,
    HTTPException,
    Depends
)

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse

import bcrypt
import jwt

from domain.models_domain import (
    UsuarioCreate,
    LoginRequest,
    AsignarRolRequest
)

from service.usuario_service import UsuarioService
from repositories import usuario_repo  # ← USAR EL REPOSITORIO CENTRAL


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
    except Exception:
        return None


service = UsuarioService(usuario_repo)

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_usuario(
    data: UsuarioCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "Usuario no autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Token inválido o expirado",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    if usuario.get('id_rol') != 1:
        raise HTTPException(
            status_code=403,
            detail={
                "success": False,
                "statusCode": 403,
                "message": "Acceso denegado",
                "error": {
                    "error_code": "ACCESO_DENEGADO",
                    "details": "Se requiere rol de administrador",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    if not data.telefono:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "CAMPO_REQUERIDO",
                    "details": "El campo telefono es obligatorio",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    if "@" not in data.email or "." not in data.email:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "INVALID_DATA",
                    "details": "El email no tiene un formato válido",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    if usuario_repo.existe_por_email(data.email):
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "EMAIL_DUPLICADO",
                    "details": f"El email {data.email} ya está registrado",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    if len(data.password) < 6:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "INVALID_DATA",
                    "details": "La contraseña debe tener mínimo 6 caracteres",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    if data.id_rol not in [1, 2]:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "ROL_INVALIDO",
                    "details": "El rol debe ser 1 (administrador) o 2 (residente)",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    password_hash = bcrypt.hashpw(
        data.password.encode("utf-8"),
        bcrypt.gensalt(rounds=10)
    ).decode("utf-8")
    
    nuevo_usuario = usuario_repo.create({
        "nombre_completo": data.nombre_completo,
        "email": data.email.lower(),
        "telefono": data.telefono,
        "password_hash": password_hash,
        "id_rol": data.id_rol,
        "activo": True,
        "intentos_fallidos": 0,
        "bloqueado_hasta": None,
        "ultimo_login": None,
        "fecha_registro": datetime.utcnow()
    })
    
    rol_nombre = "administrador" if data.id_rol == 1 else "residente"
    
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Usuario creado exitosamente",
            "data": {
                "id_usuario": nuevo_usuario["id_usuario"],
                "nombre_completo": nuevo_usuario["nombre_completo"],
                "email": nuevo_usuario["email"],
                "telefono": nuevo_usuario["telefono"],
                "id_rol": nuevo_usuario["id_rol"],
                "rol_nombre": rol_nombre,
                "activo": nuevo_usuario["activo"],
                "fecha_registro": nuevo_usuario["fecha_registro"].isoformat()
            }
        }
    )


@router.post("/login", status_code=status.HTTP_200_OK)
def login_usuario(data: LoginRequest):
    resultado = service.login(data)
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Inicio de sesión exitoso",
            "data": resultado
        }
    )


@router.patch("/{id}/rol", status_code=status.HTTP_200_OK)
def actualizar_rol(
    id: int,
    data: AsignarRolRequest,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    
    if not usuario:
        raise HTTPException(
            status_code=401,
            detail={
                "success": False,
                "statusCode": 401,
                "message": "No autenticado"
            }
        )
    
    resultado = service.actualizar_rol(
        id,
        data.id_rol,
        usuario,
        request.client.host if request.client else None
    )
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Rol actualizado exitosamente",
            "data": resultado
        }
    )


@router.get("/debug/usuarios", status_code=status.HTTP_200_OK)
def debug_usuarios(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    todos = usuario_repo.get_all()
    
    resultado = []
    for u in todos.values():
        resultado.append({
            "id_usuario": u.get("id_usuario"),
            "nombre_completo": u.get("nombre_completo"),
            "email": u.get("email"),
            "id_rol": u.get("id_rol"),
            "activo": u.get("activo"),
            "intentos_fallidos": u.get("intentos_fallidos", 0),
            "bloqueado_hasta": str(u.get("bloqueado_hasta")) if u.get("bloqueado_hasta") else None
        })
    
    return {"usuarios": resultado}


@router.patch("/debug/activar-usuario/{usuario_id}")
def activar_usuario_directo(
    usuario_id: int,
    activo: bool,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    if usuario_id in usuario_repo._db:
        usuario_repo._db[usuario_id]["activo"] = activo
        estado = "activado" if activo else "desactivado"
        return {
            "success": True,
            "message": f"Usuario {usuario_id} {estado}",
            "activo": usuario_repo._db[usuario_id]["activo"]
        }
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")