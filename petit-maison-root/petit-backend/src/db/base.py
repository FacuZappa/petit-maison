"""
Configuración base de la base de datos.
Todas las tablas y repositorios importan desde acá.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./db/petit.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    """Clase base para todos los modelos SQLAlchemy"""
    pass

def get_db():
    """Generador de sesiones de base de datos para FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
