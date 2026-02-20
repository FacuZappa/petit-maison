from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from ..dto.usuario import UsuarioCreate, UsuarioOut

DATABASE_URL = "sqlite:///./db/petit.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    telefono: Mapped[str] = mapped_column(String(30))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: UsuarioCreate) -> UsuarioDB:
        existe = self.db.query(UsuarioDB).filter(UsuarioDB.email == data.email).first()
        if existe:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        usuario = UsuarioDB(
            nombre=data.nombre,
            email=data.email,
            telefono=data.telefono
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def listar(self):
        return self.db.query(UsuarioDB).all()

    def por_email(self, email: str):
        usuario = self.db.query(UsuarioDB).filter(UsuarioDB.email == email).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario