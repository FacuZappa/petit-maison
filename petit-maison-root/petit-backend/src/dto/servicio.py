from pydantic import BaseModel
from typing import Optional

# Para CREAR un servicio
class ServicioCreate(BaseModel):
    nombre: str
    duracion_min: int  # Duración en minutos
    precio: float

# Para ACTUALIZAR un servicio
class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    duracion_min: Optional[int] = None
    precio: Optional[float] = None
    activo: Optional[bool] = None

# Para RESPONDER al usuario
class ServicioOut(BaseModel):
    id: int
    nombre: str
    duracion_min: int
    precio: float
    activo: bool

    class Config:
        from_attributes = True
