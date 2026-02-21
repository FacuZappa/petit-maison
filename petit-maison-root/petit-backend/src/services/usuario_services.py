from ..db.usuario_repository import UsuarioRepository
from ..dto.usuario import UsuarioCreate

class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def crear_usuario(self, data: UsuarioCreate):
        return self.repo.crear(data)

    def obtener_usuarios(self):
        return self.repo.listar()

    def obtener_usuario_por_email(self, email: str):
        return self.repo.por_email(email)