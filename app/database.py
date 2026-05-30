import sqlite3
from contextlib import contextmanager
from datetime import datetime

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
                rol TEXT DEFAULT 'residente',
                activo BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabla de zonas comunes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS zonas_comunes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                capacidad_maxima INTEGER NOT NULL,
                descripcion TEXT,
                estado TEXT DEFAULT 'disponible',
                horario_inicio TIME,
                horario_fin TIME,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insertar usuario administrador por defecto
        cursor.execute("""
            INSERT OR IGNORE INTO usuarios (id, nombre, email, password, rol)
            VALUES (1, 'Administrador', 'admin@admin.com', 'admin123', 'administrador')
        """)
        
        conn.commit()
        print("Base de datos inicializada correctamente")