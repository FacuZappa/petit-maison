from datetime import date
from ..db.turno_repository import TurnoRepository, TurnoDB
from ..dto.turno import TurnoCreate, TurnoUpdate, EstadoTurno


class TurnoService:
    """Servicio de lógica de negocio para turnos/agenda"""
    
    def __init__(self, repo: TurnoRepository):
        self.repo = repo

    def crear_turno(self, data: TurnoCreate) -> TurnoDB:
        """Crea un nuevo turno"""
        return self.repo.crear(data)

    def obtener_agenda_dia(self, fecha: date) -> list[dict]:
        """Obtiene la agenda de un día específico"""
        return self.repo.listar_por_fecha(fecha)

    def obtener_historial_cliente(self, cliente_id: int) -> list[dict]:
        """Obtiene el historial de turnos de un cliente"""
        return self.repo.listar_por_cliente(cliente_id)

    def obtener_turno(self, id: int) -> TurnoDB:
        """Obtiene un turno por ID"""
        return self.repo.por_id(id)

    def actualizar_turno(self, id: int, data: TurnoUpdate) -> TurnoDB:
        """Actualiza un turno"""
        return self.repo.actualizar(id, data)

    def confirmar_turno(self, id: int) -> TurnoDB:
        """Marca un turno como confirmado"""
        return self.repo.cambiar_estado(id, EstadoTurno.CONFIRMADO)

    def completar_turno(self, id: int) -> TurnoDB:
        """Marca un turno como completado"""
        return self.repo.cambiar_estado(id, EstadoTurno.COMPLETADO)

    def cancelar_turno(self, id: int) -> TurnoDB:
        """Marca un turno como cancelado"""
        return self.repo.cambiar_estado(id, EstadoTurno.CANCELADO)

    def marcar_no_asistio(self, id: int) -> TurnoDB:
        """Marca que el cliente no asistió"""
        return self.repo.cambiar_estado(id, EstadoTurno.NO_ASISTIO)

    def eliminar_turno(self, id: int) -> bool:
        """Elimina un turno"""
        return self.repo.eliminar(id)
