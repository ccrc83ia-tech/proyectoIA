from typing import List
from ..domain.entities import AgendaEvent
from ..infrastructure.ports.agenda_repository_port import AgendaRepositoryPort
from ..infrastructure.ports.service_ports import AgendaServicePort
import html
import os
from pathlib import Path

class AgendaService(AgendaServicePort):
    """Servicio de aplicación - Casos de uso de agenda"""
    
    def __init__(self, repository: AgendaRepositoryPort):
        if not repository:
            raise ValueError("Repository no puede ser None")
        self._repository = repository
    
    def _sanitize_input(self, text: str) -> str:
        """Sanitiza entrada del usuario para prevenir XSS."""
        if not isinstance(text, str):
            raise ValueError("Input debe ser string")
        return html.escape(text.strip())
    
    def create_event(self, evento: str, fecha: str, hora: str) -> str:
        """Caso de uso: Crear evento"""
        try:
            # Sanitizar entradas
            evento_clean = self._sanitize_input(evento)
            fecha_clean = self._sanitize_input(fecha)
            hora_clean = self._sanitize_input(hora)
            
            # Crear entidad de dominio (con validación automática)
            event = AgendaEvent(evento_clean, fecha_clean, hora_clean)
            
            # Persistir usando puerto de salida
            success = self._repository.save(event)
            
            if success:
                return f"Evento '{evento_clean}' agregado para {fecha_clean} a las {hora_clean}"
            else:
                return "Error al guardar el evento"
                
        except ValueError as e:
            return f"Error de validación: {str(e)}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"
    
    def get_events_by_date(self, fecha: str) -> str:
        """Caso de uso: Consultar eventos por fecha"""
        try:
            fecha_clean = self._sanitize_input(fecha)
            events = self._repository.find_by_date(fecha_clean)
            
            if not events:
                return f"No hay eventos programados para {fecha_clean}"
            
            result = f"Eventos para {fecha_clean}:\n"
            for event in events:
                result += f"- {event.evento} a las {event.hora}\n"
            
            return result
            
        except ValueError as e:
            return f"Error de validación: {str(e)}"
        except Exception as e:
            return f"Error al consultar eventos: {str(e)}"
    
    def delete_event(self, evento: str, fecha: str) -> str:
        """Caso de uso: Eliminar evento"""
        try:
            evento_clean = self._sanitize_input(evento)
            fecha_clean = self._sanitize_input(fecha)
            
            success = self._repository.delete(evento_clean, fecha_clean)
            
            if success:
                return f"Evento '{evento_clean}' eliminado de {fecha_clean}"
            else:
                return f"No se encontró el evento '{evento_clean}' en la fecha {fecha_clean}"
                
        except ValueError as e:
            return f"Error de validación: {str(e)}"
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