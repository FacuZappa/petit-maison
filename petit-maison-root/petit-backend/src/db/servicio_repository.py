from sqlalchemy import String, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, Session
from fastapi import HTTPException
from typing import Optional

from .base import Base
from ..dto.servicio import ServicioCreate, ServicioUpdate


class ServicioDB(Base):
    """Modelo de base de datos para Servicio"""
    __tablename__ = "servicios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    duracion_min: Mapped[int] = mapped_column(nullable=False)  # Duración en minutos
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)


class ServicioRepository:
    """Repositorio para operaciones CRUD de servicios"""
    
    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: ServicioCreate) -> ServicioDB:
        """Crea un nuevo servicio"""
        servicio = ServicioDB(
            nombre=data.nombre,
            duracion_min=data.duracion_min,
            precio=data.precio,
            activo=True
        )
        self.db.add(servicio)
        self.db.commit()
        self.db.refresh(servicio)
        return servicio

    def listar(self, solo_activos: bool = True) -> list[ServicioDB]:
        """Lista servicios (por defecto solo activos)"""
        query = self.db.query(ServicioDB)
        if solo_activos:
            query = query.filter(ServicioDB.activo == True)
        return query.order_by(ServicioDB.nombre).all()

    def por_id(self, id: int) -> ServicioDB:
        """Obtiene un servicio por su ID"""
        servicio = self.db.query(ServicioDB).filter(ServicioDB.id == id).first()
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return servicio

    def actualizar(self, id: int, data: ServicioUpdate) -> ServicioDB:
        """Actualiza un servicio existente"""
        servicio = self.por_id(id)
        
        if data.nombre is not None:
            servicio.nombre = data.nombre
        if data.duracion_min is not None:
            servicio.duracion_min = data.duracion_min
        if data.precio is not None:
            servicio.precio = data.precio
        if data.activo is not None:
            servicio.activo = data.activo
        
        self.db.commit()
        self.db.refresh(servicio)
        return servicio

    def desactivar(self, id: int) -> ServicioDB:
        """Desactiva un servicio (no lo elimina)"""
        servicio = self.por_id(id)
        servicio.activo = False
        self.db.commit()
        self.db.refresh(servicio)
        return servicio
