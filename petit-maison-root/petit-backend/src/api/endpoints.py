from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date

# DTOs
from ..dto.usuario import UsuarioCreate, UsuarioOut
from ..dto.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from ..dto.servicio import ServicioCreate, ServicioUpdate, ServicioOut
from ..dto.turno import TurnoCreate, TurnoUpdate, TurnoOut, TurnoDetailOut

# Base de datos
from ..db.base import Base, engine, get_db
from ..db.usuario_repository import UsuarioRepository
from ..db.cliente_repository import ClienteRepository
from ..db.servicio_repository import ServicioRepository
from ..db.turno_repository import TurnoRepository

# Servicios
from ..services.usuario_services import UsuarioService
from ..services.cliente_services import ClienteService
from ..services.servicio_services import ServicioService
from ..services.turno_services import TurnoService

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Petit Maison API", description="Sistema de gestión de turnos para manicura")


# ============== USUARIOS (existente) ==============

@app.post("/usuarios/", response_model=UsuarioOut, tags=["Usuarios"])
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuarioService(UsuarioRepository(db))
    return service.crear_usuario(data)

@app.get("/usuarios/", response_model=list[UsuarioOut], tags=["Usuarios"])
def obtener_usuarios(db: Session = Depends(get_db)):
    service = UsuarioService(UsuarioRepository(db))
    return service.obtener_usuarios()

@app.get("/usuarios/{email}", response_model=UsuarioOut, tags=["Usuarios"])
def obtener_usuario_por_email(email: str, db: Session = Depends(get_db)):
    service = UsuarioService(UsuarioRepository(db))
    return service.obtener_usuario_por_email(email)


# ============== CLIENTES ==============

@app.post("/clientes/", response_model=ClienteOut, tags=["Clientes"])
def crear_cliente(data: ClienteCreate, db: Session = Depends(get_db)):
    """Crea un nuevo cliente"""
    service = ClienteService(ClienteRepository(db))
    return service.crear_cliente(data)

@app.get("/clientes/", response_model=list[ClienteOut], tags=["Clientes"])
def obtener_clientes(db: Session = Depends(get_db)):
    """Lista todos los clientes"""
    service = ClienteService(ClienteRepository(db))
    return service.obtener_clientes()

@app.get("/clientes/buscar/{termino}", response_model=list[ClienteOut], tags=["Clientes"])
def buscar_clientes(termino: str, db: Session = Depends(get_db)):
    """Busca clientes por nombre o teléfono"""
    service = ClienteService(ClienteRepository(db))
    return service.buscar_clientes(termino)

@app.get("/clientes/{id}", response_model=ClienteOut, tags=["Clientes"])
def obtener_cliente(id: int, db: Session = Depends(get_db)):
    """Obtiene un cliente por ID"""
    service = ClienteService(ClienteRepository(db))
    return service.obtener_cliente(id)

@app.put("/clientes/{id}", response_model=ClienteOut, tags=["Clientes"])
def actualizar_cliente(id: int, data: ClienteUpdate, db: Session = Depends(get_db)):
    """Actualiza un cliente"""
    service = ClienteService(ClienteRepository(db))
    return service.actualizar_cliente(id, data)

@app.delete("/clientes/{id}", tags=["Clientes"])
def eliminar_cliente(id: int, db: Session = Depends(get_db)):
    """Elimina un cliente"""
    service = ClienteService(ClienteRepository(db))
    service.eliminar_cliente(id)
    return {"message": "Cliente eliminado"}


# ============== SERVICIOS ==============

@app.post("/servicios/", response_model=ServicioOut, tags=["Servicios"])
def crear_servicio(data: ServicioCreate, db: Session = Depends(get_db)):
    """Crea un nuevo servicio de manicura"""
    service = ServicioService(ServicioRepository(db))
    return service.crear_servicio(data)

@app.get("/servicios/", response_model=list[ServicioOut], tags=["Servicios"])
def obtener_servicios(solo_activos: bool = True, db: Session = Depends(get_db)):
    """Lista servicios (por defecto solo activos)"""
    service = ServicioService(ServicioRepository(db))
    return service.obtener_servicios(solo_activos)

@app.get("/servicios/{id}", response_model=ServicioOut, tags=["Servicios"])
def obtener_servicio(id: int, db: Session = Depends(get_db)):
    """Obtiene un servicio por ID"""
    service = ServicioService(ServicioRepository(db))
    return service.obtener_servicio(id)

@app.put("/servicios/{id}", response_model=ServicioOut, tags=["Servicios"])
def actualizar_servicio(id: int, data: ServicioUpdate, db: Session = Depends(get_db)):
    """Actualiza un servicio"""
    service = ServicioService(ServicioRepository(db))
    return service.actualizar_servicio(id, data)

@app.delete("/servicios/{id}", response_model=ServicioOut, tags=["Servicios"])
def desactivar_servicio(id: int, db: Session = Depends(get_db)):
    """Desactiva un servicio (no lo elimina)"""
    service = ServicioService(ServicioRepository(db))
    return service.desactivar_servicio(id)


# ============== TURNOS ==============

@app.post("/turnos/", response_model=TurnoOut, tags=["Turnos"])
def crear_turno(data: TurnoCreate, db: Session = Depends(get_db)):
    """Agenda un nuevo turno"""
    service = TurnoService(TurnoRepository(db))
    return service.crear_turno(data)

@app.get("/turnos/agenda/{fecha}", response_model=list[TurnoDetailOut], tags=["Turnos"])
def obtener_agenda_dia(fecha: date, db: Session = Depends(get_db)):
    """Obtiene la agenda de un día (formato: YYYY-MM-DD)"""
    service = TurnoService(TurnoRepository(db))
    return service.obtener_agenda_dia(fecha)

@app.get("/turnos/cliente/{cliente_id}", response_model=list[TurnoDetailOut], tags=["Turnos"])
def obtener_historial_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtiene el historial de turnos de un cliente"""
    service = TurnoService(TurnoRepository(db))
    return service.obtener_historial_cliente(cliente_id)

@app.get("/turnos/{id}", response_model=TurnoOut, tags=["Turnos"])
def obtener_turno(id: int, db: Session = Depends(get_db)):
    """Obtiene un turno por ID"""
    service = TurnoService(TurnoRepository(db))
    return service.obtener_turno(id)

@app.put("/turnos/{id}", response_model=TurnoOut, tags=["Turnos"])
def actualizar_turno(id: int, data: TurnoUpdate, db: Session = Depends(get_db)):
    """Actualiza un turno"""
    service = TurnoService(TurnoRepository(db))
    return service.actualizar_turno(id, data)

@app.post("/turnos/{id}/confirmar", response_model=TurnoOut, tags=["Turnos"])
def confirmar_turno(id: int, db: Session = Depends(get_db)):
    """Confirma un turno"""
    service = TurnoService(TurnoRepository(db))
    return service.confirmar_turno(id)

@app.post("/turnos/{id}/completar", response_model=TurnoOut, tags=["Turnos"])
def completar_turno(id: int, db: Session = Depends(get_db)):
    """Marca un turno como completado"""
    service = TurnoService(TurnoRepository(db))
    return service.completar_turno(id)

@app.post("/turnos/{id}/cancelar", response_model=TurnoOut, tags=["Turnos"])
def cancelar_turno(id: int, db: Session = Depends(get_db)):
    """Cancela un turno"""
    service = TurnoService(TurnoRepository(db))
    return service.cancelar_turno(id)

@app.post("/turnos/{id}/no-asistio", response_model=TurnoOut, tags=["Turnos"])
def marcar_no_asistio(id: int, db: Session = Depends(get_db)):
    """Marca que el cliente no asistió"""
    service = TurnoService(TurnoRepository(db))
    return service.marcar_no_asistio(id)

@app.delete("/turnos/{id}", tags=["Turnos"])
def eliminar_turno(id: int, db: Session = Depends(get_db)):
    """Elimina un turno"""
    service = TurnoService(TurnoRepository(db))
    service.eliminar_turno(id)
    return {"message": "Turno eliminado"}