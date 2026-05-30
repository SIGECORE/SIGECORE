from app.database import get_db

class ZonaRepository:
    
    def get_all(self):
        """Obtener todas las zonas"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM zonas_comunes ORDER BY id")
            return cursor.fetchall()
    
    def get_by_id(self, zona_id):
        """Obtener zona por ID"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM zonas_comunes WHERE id = ?", (zona_id,))
            return cursor.fetchone()
    
    def create(self, nombre, descripcion, capacidad):
        """Crear nueva zona"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO zonas_comunes (nombre, descripcion, capacidad, estado)
                VALUES (?, ?, ?, 'disponible')
            """, (nombre, descripcion, capacidad))
            conn.commit()
            return cursor.lastrowid
    
    def update(self, zona_id, nombre=None, descripcion=None, capacidad=None, estado=None):
        """Actualizar zona"""
        with get_db() as conn:
            cursor = conn.cursor()
            updates = []
            params = []
            
            if nombre is not None:
                updates.append("nombre = ?")
                params.append(nombre)
            if descripcion is not None:
                updates.append("descripcion = ?")
                params.append(descripcion)
            if capacidad is not None:
                updates.append("capacidad = ?")
                params.append(capacidad)
            if estado is not None:
                updates.append("estado = ?")
                params.append(estado)
            
            if not updates:
                return False
            
            params.append(zona_id)
            query = f"UPDATE zonas_comunes SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
    
    def delete(self, zona_id):
        """Eliminar zona"""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM zonas_comunes WHERE id = ?", (zona_id,))
            conn.commit()
            return cursor.rowcount > 0