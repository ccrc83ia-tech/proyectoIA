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
    
    @abstractmethod
    def delete_all(self) -> bool:
        """Elimina todos los eventos"""
        pass
    
    @abstractmethod
    def export_to_excel(self, export_path: str) -> bool:
        """Exporta la agenda a un archivo Excel específico"""
        pass