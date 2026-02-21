from ..db.servicio_repository import ServicioRepository, ServicioDB
from ..dto.servicio import ServicioCreate, ServicioUpdate


class ServicioService:
    """Servicio de lógica de negocio para servicios de manicura"""
    
    def __init__(self, repo: ServicioRepository):
        self.repo = repo

    def crear_servicio(self, data: ServicioCreate) -> ServicioDB:
        """Crea un nuevo servicio"""
        return self.repo.crear(data)

    def obtener_servicios(self, solo_activos: bool = True) -> list[ServicioDB]:
        """Obtiene todos los servicios (por defecto solo activos)"""
        return self.repo.listar(solo_activos)

    def obtener_servicio(self, id: int) -> ServicioDB:
        """Obtiene un servicio por ID"""
        return self.repo.por_id(id)

    def actualizar_servicio(self, id: int, data: ServicioUpdate) -> ServicioDB:
        """Actualiza un servicio"""
        return self.repo.actualizar(id, data)

    def desactivar_servicio(self, id: int) -> ServicioDB:
        """Desactiva un servicio (no lo elimina para mantener historial)"""
        return self.repo.desactivar(id)
