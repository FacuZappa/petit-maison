from fastapi import HTTPException
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, Session
from ..dto.usuario import UsuarioCreate
from .base import Base, get_db, engine, SessionLocal


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    telefono: Mapped[str] = mapped_column(String(30))
        
        
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