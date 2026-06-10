from datetime import datetime, timezone
from typing import Optional, List
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
import jwt
from pydantic import BaseModel

SECRET_KEY = "mi_clave_secreta"
security = HTTPBearer()


class ComunicadoCreate(BaseModel):
    titulo: str
    contenido: str
    archivos_adjuntos: Optional[List[str]] = []
    fecha_expiracion: Optional[datetime] = None


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


# Repositorio en memoria
comunicados_db = {}
next_id = 1

router = APIRouter(tags=["Comunicados"])


# ==================== POST /comunicados ====================
@router.post("/comunicados", status_code=status.HTTP_201_CREATED)
def publicar_comunicado(
    data: ComunicadoCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    global next_id, comunicados_db
    
    token = credentials.credentials
    usuario = validar_token(token)
    
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
                    "timestamp": datetime.now(timezone.utc).isoformat()
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
                    "details": "Se requiere rol de administrador para publicar comunicados",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    if not data.titulo or data.titulo.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "CAMPO_REQUERIDO",
                    "details": "El campo titulo es obligatorio",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    if not data.contenido or data.contenido.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "statusCode": 400,
                "message": "Error en la solicitud",
                "error": {
                    "error_code": "CAMPO_REQUERIDO",
                    "details": "El campo contenido es obligatorio",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    if data.fecha_expiracion:
        if data.fecha_expiracion.tzinfo is None:
            fecha_expiracion = data.fecha_expiracion.replace(tzinfo=timezone.utc)
        else:
            fecha_expiracion = data.fecha_expiracion
        
        ahora = datetime.now(timezone.utc)
        
        if fecha_expiracion < ahora:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "statusCode": 400,
                    "message": "Error en la solicitud",
                    "error": {
                        "error_code": "FECHA_EXPIRACION_INVALIDA",
                        "details": "La fecha de expiración no puede ser anterior a la fecha actual",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                }
            )
    
    comunicado = {
        "id_comunicado": next_id,
        "titulo": data.titulo,
        "contenido": data.contenido,
        "id_autor": usuario.get('id_usuario'),
        "autor_nombre": usuario.get('nombre_completo'),
        "archivos_adjuntos": data.archivos_adjuntos if data.archivos_adjuntos else [],
        "fecha_publicacion": datetime.now(timezone.utc),
        "fecha_expiracion": data.fecha_expiracion,
        "activo": True
    }
    
    comunicados_db[next_id] = comunicado
    next_id += 1
    
    return JSONResponse(
        status_code=201,
        content={
            "success": True,
            "statusCode": 201,
            "message": "Comunicado publicado exitosamente",
            "data": {
                "id_comunicado": comunicado["id_comunicado"],
                "titulo": comunicado["titulo"],
                "contenido": comunicado["contenido"],
                "id_autor": comunicado["id_autor"],
                "autor_nombre": comunicado["autor_nombre"],
                "archivos_adjuntos": comunicado["archivos_adjuntos"],
                "fecha_publicacion": comunicado["fecha_publicacion"].isoformat(),
                "fecha_expiracion": comunicado["fecha_expiracion"].isoformat() if comunicado["fecha_expiracion"] else None,
                "activo": comunicado["activo"]
            }
        }
    )


# ==================== GET /comunicados/activos ====================
@router.get("/comunicados/activos", status_code=status.HTTP_200_OK)
def listar_comunicados_activos(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    global comunicados_db
    
    token = credentials.credentials
    usuario = validar_token(token)
    
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
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
        )
    
    ahora = datetime.now(timezone.utc)
    
    # Filtrar comunicados activos
    activos = []
    for comunicado in comunicados_db.values():
        if not comunicado["activo"]:
            continue
        
        fecha_expiracion = comunicado["fecha_expiracion"]
        if fecha_expiracion:
            if fecha_expiracion.tzinfo is None:
                fecha_expiracion = fecha_expiracion.replace(tzinfo=timezone.utc)
            
            if fecha_expiracion < ahora:
                continue
        
        activos.append(comunicado)
    
    # Ordenar por fecha de publicación descendente
    activos.sort(key=lambda x: x["fecha_publicacion"], reverse=True)
    
    resultado = []
    for c in activos:
        resultado.append({
            "id_comunicado": c["id_comunicado"],
            "titulo": c["titulo"],
            "contenido": c["contenido"],
            "autor": {
                "id_autor": c["id_autor"],
                "nombre": c["autor_nombre"]
            },
            "archivos_adjuntos": c["archivos_adjuntos"],
            "fecha_publicacion": c["fecha_publicacion"].isoformat()
        })
    
    if len(resultado) == 0:
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "statusCode": 200,
                "message": "No hay comunicados activos en este momento",
                "data": {
                    "comunicados": []
                }
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "statusCode": 200,
            "message": "Consulta exitosa",
            "data": {
                "comunicados": resultado
            }
        }
    )
@router.patch("/comunicados/debug/{comunicado_id}/desactivar")
def desactivar_comunicado(
    comunicado_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    global comunicados_db
    
    usuario = validar_token(credentials.credentials)
    if not usuario or usuario.get('id_rol') != 1:
        raise HTTPException(status_code=403, detail="Acceso denegado")
    
    if comunicado_id not in comunicados_db:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")
    
    comunicados_db[comunicado_id]["activo"] = False
    
    return {"message": f"Comunicado {comunicado_id} desactivado"}