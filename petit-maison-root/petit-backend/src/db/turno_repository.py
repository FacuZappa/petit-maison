from sqlalchemy import String, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.sql import func
from fastapi import HTTPException
from typing import Optional
from datetime import date, time, datetime

from .base import Base
from .cliente_repository import ClienteDB
from .servicio_repository import ServicioDB
from ..dto.turno import TurnoCreate, TurnoUpdate, EstadoTurno


class TurnoDB(Base):
    """Modelo de base de datos para Turno"""
    __tablename__ = "turnos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    servicio_id: Mapped[int] = mapped_column(ForeignKey("servicios.id"), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    notas: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class TurnoRepository:
    """Repositorio para operaciones CRUD de turnos"""
    
    def __init__(self, db: Session):
        self.db = db

    def crear(self, data: TurnoCreate) -> TurnoDB:
        """Crea un nuevo turno"""
        # Verificar que existen cliente y servicio
        cliente = self.db.query(ClienteDB).filter(ClienteDB.id == data.cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
        servicio = self.db.query(ServicioDB).filter(ServicioDB.id == data.servicio_id).first()
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        turno = TurnoDB(
            cliente_id=data.cliente_id,
            servicio_id=data.servicio_id,
            fecha=data.fecha,
            hora_inicio=data.hora_inicio,
            estado=EstadoTurno.PENDIENTE.value,
            notas=data.notas
        )
        self.db.add(turno)
        self.db.commit()
        self.db.refresh(turno)
        return turno

    def listar_por_fecha(self, fecha: date) -> list[dict]:
        """Lista todos los turnos de una fecha con detalles"""
        turnos = self.db.query(
            TurnoDB, ClienteDB, ServicioDB
        ).join(
            ClienteDB, TurnoDB.cliente_id == ClienteDB.id
        ).join(
            ServicioDB, TurnoDB.servicio_id == ServicioDB.id
        ).filter(
            TurnoDB.fecha == fecha
        ).order_by(
            TurnoDB.hora_inicio
        ).all()

        return [self._turno_to_detail(t, c, s) for t, c, s in turnos]

    def listar_por_cliente(self, cliente_id: int) -> list[dict]:
        """Lista el historial de turnos de un cliente"""
        turnos = self.db.query(
            TurnoDB, ClienteDB, ServicioDB
        ).join(
            ClienteDB, TurnoDB.cliente_id == ClienteDB.id
        ).join(
            ServicioDB, TurnoDB.servicio_id == ServicioDB.id
        ).filter(
            TurnoDB.cliente_id == cliente_id
        ).order_by(
            TurnoDB.fecha.desc(), TurnoDB.hora_inicio.desc()
        ).all()

        return [self._turno_to_detail(t, c, s) for t, c, s in turnos]

    def por_id(self, id: int) -> TurnoDB:
        """Obtiene un turno por su ID"""
        turno = self.db.query(TurnoDB).filter(TurnoDB.id == id).first()
        if not turno:
            raise HTTPException(status_code=404, detail="Turno no encontrado")
        return turno

    def actualizar(self, id: int, data: TurnoUpdate) -> TurnoDB:
        """Actualiza un turno existente"""
        turno = self.por_id(id)
        
        if data.cliente_id is not None:
            turno.cliente_id = data.cliente_id
        if data.servicio_id is not None:
            turno.servicio_id = data.servicio_id
        if data.fecha is not None:
            turno.fecha = data.fecha
        if data.hora_inicio is not None:
            turno.hora_inicio = data.hora_inicio
        if data.estado is not None:
            turno.estado = data.estado.value
        if data.notas is not None:
            turno.notas = data.notas
        
        self.db.commit()
        self.db.refresh(turno)
        return turno

    def cambiar_estado(self, id: int, estado: EstadoTurno) -> TurnoDB:
        """Cambia el estado de un turno"""
        turno = self.por_id(id)
        turno.estado = estado.value
        self.db.commit()
        self.db.refresh(turno)
        return turno

    def eliminar(self, id: int) -> bool:
        """Elimina un turno"""
        turno = self.por_id(id)
        self.db.delete(turno)
        self.db.commit()
        return True

    def _turno_to_detail(self, turno: TurnoDB, cliente: ClienteDB, servicio: ServicioDB) -> dict:
        """Convierte un turno con sus relaciones a un diccionario detallado"""
        return {
            "id": turno.id,
            "fecha": turno.fecha,
            "hora_inicio": turno.hora_inicio,
            "estado": turno.estado,
            "notas": turno.notas,
            "cliente_nombre": cliente.nombre,
            "cliente_telefono": cliente.telefono,
            "servicio_nombre": servicio.nombre,
            "servicio_duracion_min": servicio.duracion_min,
            "servicio_precio": servicio.precio
        }
