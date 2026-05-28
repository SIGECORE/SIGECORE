from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos - Cambia según tu configuración
# SQLite: sqlite:///./zonas_comunes.db
# PostgreSQL: postgresql://usuario:password@localhost/dbname
# MySQL: mysql+pymysql://usuario:password@localhost/dbname
DATABASE_URL = "sqlite:///./zonas_comunes.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependencia para obtener la sesión de la base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()