from ..db.cliente_repository import ClienteRepository, ClienteDB
from ..dto.cliente import ClienteCreate, ClienteUpdate


class ClienteService:
    """Servicio de lógica de negocio para clientes"""
    
    def __init__(self, repo: ClienteRepository):
        self.repo = repo

    def crear_cliente(self, data: ClienteCreate) -> ClienteDB:
        """Crea un nuevo cliente"""
        return self.repo.crear(data)

    def obtener_clientes(self) -> list[ClienteDB]:
        """Obtiene todos los clientes"""
        return self.repo.listar()

    def obtener_cliente(self, id: int) -> ClienteDB:
        """Obtiene un cliente por ID"""
        return self.repo.por_id(id)

    def buscar_clientes(self, termino: str) -> list[ClienteDB]:
        """Busca clientes por nombre o teléfono"""
        return self.repo.buscar(termino)

    def actualizar_cliente(self, id: int, data: ClienteUpdate) -> ClienteDB:
        """Actualiza un cliente"""
        return self.repo.actualizar(id, data)

    def eliminar_cliente(self, id: int) -> bool:
        """Elimina un cliente"""
        return self.repo.eliminar(id)
