from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from ..dto.usuario import UsuarioCreate, UsuarioOut
from ..db.usuario_repository import get_db, UsuarioRepository
from ..services.usuario import UsuarioService

app = FastAPI()

@app.post("/usuarios/", response_model=UsuarioOut)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuarioService(UsuarioRepository(db))
    return service.crear_usuario(data)

@app.get("/usuarios/", response_model=list[UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    service = UsuarioService(UsuarioRepository(db))
    return service.obtener_usuarios()

@app.get("/usuarios/{email}", response_model=UsuarioOut)
def obtener_usuario_por_email(email: str, db: Session = Depends(get_db)):
    service = UsuarioService(UsuarioRepository(db))
    return service.obtener_usuario_por_email(email)