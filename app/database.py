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
        
        # Eliminar tablas si existen para recrearlas limpias
        cursor.execute("DROP TABLE IF EXISTS reservas")
        cursor.execute("DROP TABLE IF EXISTS zonas_comunes")
        cursor.execute("DROP TABLE IF EXISTS usuarios")
        
        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE usuarios (
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
            CREATE TABLE zonas_comunes (
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
        
        # Tabla de reservas
        cursor.execute("""
            CREATE TABLE reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zona_id INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                estado TEXT DEFAULT 'pendiente',
                observaciones TEXT,
                fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (zona_id) REFERENCES zonas_comunes(id),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """)
        
        # Insertar usuario administrador por defecto
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, email, password, rol)
            VALUES (1, 'Administrador', 'admin@admin.com', 'admin123', 'administrador')
        """)
        
        # Insertar usuario residente de prueba
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, email, password, rol)
            VALUES (2, 'Carlos Rodríguez', 'carlos@test.com', '123456', 'residente')
        """)
        
        conn.commit()
        print("Base de datos inicializada correctamente")
        print("- Usuario admin: admin@admin.com / admin123")
        print("- Usuario residente: carlos@test.com / 123456")