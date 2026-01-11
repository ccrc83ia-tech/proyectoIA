from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.entities import AgendaEvent

class AgendaRepositoryPort(ABC):
    """Puerto de salida - Interfaz del repositorio de agenda"""
    
    @abstractmethod
    def save(self, event: AgendaEvent) -> bool:
        """Guarda un evento en el repositorio"""
        pass
    
    @abstractmethod
    def find_by_date(self, fecha: str) -> List[AgendaEvent]:
        """Encuentra eventos por fecha"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[AgendaEvent]:
        """Encuentra todos los eventos"""
        pass
    
    @abstractmethod
    def delete(self, evento: str, fecha: str) -> bool:
        """Elimina un evento específico"""
        pass