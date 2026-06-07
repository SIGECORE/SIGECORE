# app/api/v1/zonas.py
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime
import jwt

router = APIRouter(tags=["Zonas Comunes"])

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


@router.get("/zonas/disponibilidad")
def consultar_disponibilidad(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    zona_id: int = Query(..., description="ID de la zona común"),
    fecha: str = Query(..., description="Fecha (YYYY-MM-DD)"),
    hora_inicio: str = Query(..., description="Hora inicio (HH:MM)"),
    hora_fin: str = Query(..., description="Hora fin (HH:MM)")
):
    token = credentials.credentials
    usuario = validar_token(token)
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Validar fecha
    try:
        fecha_actual = datetime.now().date()
        fecha_consulta = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_consulta < fecha_actual:
            raise HTTPException(status_code=400, detail="La fecha no puede ser anterior a la fecha actual")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")
    
    # Validar horario
    if hora_inicio >= hora_fin:
        raise HTTPException(status_code=400, detail="La hora de inicio debe ser menor que la hora de fin")
    
    # Respuesta simulada (por ahora)
    return {
        "success": True,
        "statusCode": 200,
        "message": "La zona está disponible",
        "data": {
            "zona_id": zona_id,
            "nombre": "Salón Social",
            "fecha": fecha,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "disponible": True,
            "conflicto_con": None
        }
    }