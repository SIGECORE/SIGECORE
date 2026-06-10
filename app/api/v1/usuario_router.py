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
from repository.usuario_repository import UsuarioRepository


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


repo = UsuarioRepository()
service = UsuarioService(repo)

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
    
    if repo.existe_por_email(data.email):
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
    
    nuevo_usuario = repo.create({
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
                "message": "No autenticado",
                "error": {
                    "error_code": "NO_AUTENTICADO",
                    "details": "Se requiere un token de autenticación válido",
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
                    "details": "Se requiere rol de administrador para realizar esta acción",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    user = repo.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "statusCode": 404,
                "message": "Usuario no encontrado",
                "error": {
                    "error_code": "USUARIO_NOT_FOUND",
                    "details": f"No existe un usuario con el ID {id}",
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
    
    if usuario.get('id_usuario') == id:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "AUTO_MODIFICACION_NO_PERMITIDA",
                    "details": "No puedes cambiar tu propio rol de administrador",
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
    
    rol_anterior = user["id_rol"]
    user["id_rol"] = data.id_rol
    repo.actualizar(user)
    
    auditoria = {
        "id_usuario_modificado": id,
        "rol_anterior": rol_anterior,
        "rol_nuevo": data.id_rol,
        "id_usuario_modificador": usuario.get('id_usuario'),
        "ip_origen": request.client.host if request.client else None,
        "fecha": datetime.utcnow()
    }
    repo.registrar_auditoria(auditoria)
    
    rol_nombre = "administrador" if data.id_rol == 1 else "residente"
    modificador_nombre = usuario.get('nombre_completo', 'Administrador')
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Rol actualizado exitosamente",
            "data": {
                "id_usuario": user["id_usuario"],
                "nombre_completo": user["nombre_completo"],
                "email": user["email"],
                "id_rol": user["id_rol"],
                "rol_nombre": rol_nombre,
                "actualizado_por": f"{modificador_nombre} (ID: {usuario.get('id_usuario')})"
            }
        }
    )


@router.get("/debug/usuarios", status_code=status.HTTP_200_OK)
def debug_usuarios(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    todos = repo.get_all()
    
    resultado = []
    for u in todos.values():
        resultado.append({
            "id_usuario": u["id_usuario"],
            "nombre_completo": u["nombre_completo"],
            "email": u["email"],
            "password_hash": u["password_hash"][:20] + "...",
            "id_rol": u["id_rol"],
            "activo": u["activo"],
            "intentos_fallidos": u.get("intentos_fallidos", 0),
            "bloqueado_hasta": str(u.get("bloqueado_hasta")) if u.get("bloqueado_hasta") else None
        })
    
    return {"usuarios": resultado}


@router.patch("/debug/{usuario_id}/desactivar")
def desactivar_usuario(
    usuario_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    user = repo.get_by_id(usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user["activo"] = False
    repo.actualizar(user)
    
    return {"message": f"Usuario {usuario_id} desactivado"}


@router.patch("/debug/{usuario_id}/activar")
def activar_usuario(
    usuario_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    user = repo.get_by_id(usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user["activo"] = True
    repo.actualizar(user)
    
    return {"message": f"Usuario {usuario_id} activado"}


@router.patch("/debug/{usuario_id}/reset")
def resetear_usuario(
    usuario_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    user = repo.get_by_id(usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user["intentos_fallidos"] = 0
    user["bloqueado_hasta"] = None
    user["activo"] = True
    repo.actualizar(user)
    
    return {"message": f"Usuario {usuario_id} reseteado"}

@router.get("/debug/auditoria")
def debug_auditoria(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    usuario = validar_token(credentials.credentials)
    
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    # Retornar la auditoría desde el repositorio
    return {"auditoria": repo.get_auditoria()}