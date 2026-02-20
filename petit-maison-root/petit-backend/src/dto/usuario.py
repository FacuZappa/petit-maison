from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    telefono: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    telefono: str

    class Config:
        from_attributes = True