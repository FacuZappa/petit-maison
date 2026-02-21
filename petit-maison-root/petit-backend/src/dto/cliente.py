from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Para CREAR un cliente (lo que envía el usuario)
class ClienteCreate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    notas: Optional[str] = None

# Para ACTUALIZAR un cliente (todos los campos opcionales)
class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    notas: Optional[str] = None

# Para RESPONDER al usuario (lo que devuelve la API)
class ClienteOut(BaseModel):
    id: int
    nombre: str
    telefono: Optional[str]
    email: Optional[str]
    notas: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy
