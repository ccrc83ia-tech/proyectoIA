from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class AgendaEvent:
    """Entidad de dominio - Evento de agenda"""
    evento: str
    fecha: str
    hora: str

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Valida el formato de fecha y hora"""
        try:
            datetime.fromisoformat(self.fecha)
        except ValueError:
            raise ValueError(f"Fecha inválida: {self.fecha}. Use formato YYYY-MM-DD")
        
        try:
            datetime.strptime(self.hora, '%H:%M')
        except ValueError:
            raise ValueError(f"Hora inválida: {self.hora}. Use formato HH:MM")

    def to_dict(self) -> dict:
        return {
            'Evento': self.evento,
            'Fecha': self.fecha,
            'Hora': self.hora
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AgendaEvent':
        # Validar claves requeridas
        required_keys = ['Evento', 'Fecha', 'Hora']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Clave requerida '{key}' no encontrada")
        
        return cls(
            evento=data['Evento'],
            fecha=data['Fecha'],
            hora=data['Hora']
        )


@dataclass
class EventQuery:
    """Value Object para consultas"""
    fecha: Optional[str] = None
    evento: Optional[str] = None
    
    def __post_init__(self):
        if self.fecha:
            try:
                datetime.fromisoformat(self.fecha)
            except ValueError:
                raise ValueError(f"Fecha inválida: {self.fecha}. Use formato YYYY-MM-DD")
