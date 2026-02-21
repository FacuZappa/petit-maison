from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.sql import func
from fastapi import HTTPException
from typing import Optional
from datetime import datetime

from .base import Base
from ..dto.cliente import ClienteCreate, ClienteUpdate


class ClienteDB(Base):
    """Modelo de base de datos para Cliente"""
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    notas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class ClienteRepository:
    """Repositorio para operaciones CRUD de clientes"""
    
    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: ClienteCreate) -> ClienteDB:
        """Crea un nuevo cliente"""
        cliente = ClienteDB(
            nombre=data.nombre,
            telefono=data.telefono,
            email=data.email,
            notas=data.notas
        )
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def listar(self) -> list[ClienteDB]:
        """Lista todos los clientes"""
        return self.db.query(ClienteDB).order_by(ClienteDB.nombre).all()

    def por_id(self, id: int) -> ClienteDB:
        """Obtiene un cliente por su ID"""
        cliente = self.db.query(ClienteDB).filter(ClienteDB.id == id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente

    def buscar(self, termino: str) -> list[ClienteDB]:
        """Busca clientes por nombre o teléfono"""
        return self.db.query(ClienteDB).filter(
            (ClienteDB.nombre.ilike(f"%{termino}%")) |
            (ClienteDB.telefono.ilike(f"%{termino}%"))
        ).all()

    def actualizar(self, id: int, data: ClienteUpdate) -> ClienteDB:
        """Actualiza un cliente existente"""
        cliente = self.por_id(id)
        
        # Solo actualiza los campos que vienen con valor
        if data.nombre is not None:
            cliente.nombre = data.nombre
        if data.telefono is not None:
            cliente.telefono = data.telefono
        if data.email is not None:
            cliente.email = data.email
        if data.notas is not None:
            cliente.notas = data.notas
        
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def eliminar(self, id: int) -> bool:
        """Elimina un cliente"""
        cliente = self.por_id(id)
        self.db.delete(cliente)
        self.db.commit()
        return True
