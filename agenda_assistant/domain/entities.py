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
            datetime.strptime(self.fecha, '%Y-%m-%d')
            datetime.strptime(self.hora, '%H:%M')
        except ValueError as e:
            raise ValueError(f"Formato inválido: {str(e)}")

    def to_dict(self) -> dict:
        return {
            'Evento': self.evento,
            'Fecha': self.fecha,
            'Hora': self.hora
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AgendaEvent':
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
