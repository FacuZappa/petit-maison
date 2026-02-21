from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional
from enum import Enum

# Estados posibles del turno
class EstadoTurno(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"
    NO_ASISTIO = "no_asistio"

# Para CREAR un turno
class TurnoCreate(BaseModel):
    cliente_id: int
    servicio_id: int
    fecha: date           # Ej: "2026-02-20"
    hora_inicio: time     # Ej: "10:00"
    notas: Optional[str] = None

# Para ACTUALIZAR un turno
class TurnoUpdate(BaseModel):
    cliente_id: Optional[int] = None
    servicio_id: Optional[int] = None
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    estado: Optional[EstadoTurno] = None
    notas: Optional[str] = None

# Para RESPONDER (básico)
class TurnoOut(BaseModel):
    id: int
    cliente_id: int
    servicio_id: int
    fecha: date
    hora_inicio: time
    estado: str
    notas: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Para RESPONDER con detalles (incluye nombre de cliente y servicio)
class TurnoDetailOut(BaseModel):
    id: int
    fecha: date
    hora_inicio: time
    estado: str
    notas: Optional[str]
    cliente_nombre: str
    cliente_telefono: Optional[str]
    servicio_nombre: str
    servicio_duracion_min: int
    servicio_precio: float

    class Config:
        from_attributes = True
