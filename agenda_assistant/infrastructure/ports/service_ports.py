from abc import ABC, abstractmethod
from typing import List
from ...domain.entities import AgendaEvent

class AgendaServicePort(ABC):
    """Puerto de entrada - Interfaz de servicios de agenda"""
    
    @abstractmethod
    def create_event(self, evento: str, fecha: str, hora: str) -> str:
        """Crea un nuevo evento"""
        pass
    
    @abstractmethod
    def get_events_by_date(self, fecha: str) -> str:
        """Obtiene eventos por fecha"""
        pass
    
    @abstractmethod
    def delete_event(self, evento: str, fecha: str) -> str:
        """Elimina un evento"""
        pass
    
    @abstractmethod
    def get_all_events(self) -> str:
        """Obtiene todos los eventos"""
        pass

class AIAgentPort(ABC):
    """Puerto de entrada - Interfaz del agente de IA"""
    
    @abstractmethod
    def process_natural_language(self, query: str) -> str:
        """Procesa consulta en lenguaje natural"""
        pass