from typing import List
from ..domain.entities import AgendaEvent
from ..infrastructure.ports.agenda_repository_port import AgendaRepositoryPort
from ..infrastructure.ports.service_ports import AgendaServicePort

class AgendaService(AgendaServicePort):
    """Servicio de aplicación - Casos de uso de agenda"""
    
    def __init__(self, repository: AgendaRepositoryPort):
        self._repository = repository
    
    def create_event(self, evento: str, fecha: str, hora: str) -> str:
        """Caso de uso: Crear evento"""
        try:
            # Crear entidad de dominio (con validación automática)
            event = AgendaEvent(evento, fecha, hora)
            
            # Persistir usando puerto de salida
            success = self._repository.save(event)
            
            if success:
                return f"Evento '{evento}' agregado para {fecha} a las {hora}"
            else:
                return "Error al guardar el evento"
                
        except ValueError as e:
            return f"Error de validación: {str(e)}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"
    
    def get_events_by_date(self, fecha: str) -> str:
        """Caso de uso: Consultar eventos por fecha"""
        try:
            events = self._repository.find_by_date(fecha)
            
            if not events:
                return f"No hay eventos programados para {fecha}"
            
            result = f"Eventos para {fecha}:\n"
            for event in events:
                result += f"- {event.evento} a las {event.hora}\n"
            
            return result
            
        except Exception as e:
            return f"Error al consultar eventos: {str(e)}"
    
    def delete_event(self, evento: str, fecha: str) -> str:
        """Caso de uso: Eliminar evento"""
        try:
            success = self._repository.delete(evento, fecha)
            
            if success:
                return f"Evento '{evento}' eliminado de {fecha}"
            else:
                return f"No se encontró el evento '{evento}' en la fecha {fecha}"
                
        except Exception as e:
            return f"Error al eliminar evento: {str(e)}"
    
    def get_all_events(self) -> str:
        """Caso de uso: Obtener todos los eventos"""
        try:
            events = self._repository.find_all()
            
            if not events:
                return "No hay eventos en la agenda"
            
            result = "Todos los eventos:\n"
            for event in events:
                result += f"- {event.evento} el {event.fecha} a las {event.hora}\n"
            
            return result
            
        except Exception as e:
            return f"Error al obtener eventos: {str(e)}"