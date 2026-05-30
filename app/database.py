import sqlite3
from contextlib import contextmanager

DATABASE_URL = "zonas_comunes.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Inicializar la base de datos con las tablas necesarias"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                telefono TEXT,
                rol TEXT DEFAULT 'residente',
                activo BOOLEAN DEFAULT 1,
                tiene_morosidad BOOLEAN DEFAULT 0
            )
        """)
        
        # Tabla de zonas comunes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS zonas_comunes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                capacidad INTEGER,
                estado TEXT DEFAULT 'disponible'
            )
        """)
        
        # Tabla de reservas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zona_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                observaciones TEXT,
                fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_aprobacion TIMESTAMP,
                aprobado_por INTEGER,
                fecha_cancelacion TIMESTAMP,
                cancelado_por INTEGER,
                FOREIGN KEY (zona_id) REFERENCES zonas_comunes(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        
        conn.commit()
        print("Base de datos inicializada correctamente")