from app.database import get_db
from datetime import datetime

class ZonaRepository:
    
    def get_by_nombre(self, nombre):
        """Verificar si ya existe una zona con el mismo nombre"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM zonas_comunes WHERE nombre = ?", (nombre,))
            return cursor.fetchone()
    
    def create(self, nombre, capacidad_maxima, descripcion, horario_inicio, horario_fin):
        """Crear una nueva zona común"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO zonas_comunes (nombre, capacidad_maxima, descripcion, horario_inicio, horario_fin, estado, fecha_registro)
                VALUES (?, ?, ?, ?, ?, 'disponible', ?)
            """, (nombre, capacidad_maxima, descripcion, horario_inicio, horario_fin, datetime.now()))
            conn.commit()
            
            # Obtener la zona creada
            zona_id = cursor.lastrowid
            cursor.execute("SELECT * FROM zonas_comunes WHERE id = ?", (zona_id,))
            return cursor.fetchone()