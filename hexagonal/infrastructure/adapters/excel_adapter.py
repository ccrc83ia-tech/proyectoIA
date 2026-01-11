import pandas as pd
import os
from typing import List
from ..ports.agenda_repository_port import AgendaRepositoryPort
from ...domain.entities import AgendaEvent

class ExcelAgendaAdapter(AgendaRepositoryPort):
    """Adaptador de salida - Implementación para Excel"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Asegura que el archivo Excel existe"""
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['Evento', 'Fecha', 'Hora'])
            df.to_excel(self.file_path, index=False)
    
    def _load_dataframe(self) -> pd.DataFrame:
        """Carga el DataFrame desde Excel"""
        return pd.read_excel(self.file_path)
    
    def _save_dataframe(self, df: pd.DataFrame):
        """Guarda el DataFrame en Excel"""
        df.to_excel(self.file_path, index=False)
    
    def save(self, event: AgendaEvent) -> bool:
        """Implementa el puerto: guardar evento"""
        try:
            df = self._load_dataframe()
            new_row = pd.DataFrame([event.to_dict()])
            df = pd.concat([df, new_row], ignore_index=True)
            self._save_dataframe(df)
            return True
        except Exception:
            return False
    
    def find_by_date(self, fecha: str) -> List[AgendaEvent]:
        """Implementa el puerto: buscar por fecha"""
        try:
            df = self._load_dataframe()
            filtered_df = df[df['Fecha'] == fecha]
            return [AgendaEvent.from_dict(row) for _, row in filtered_df.iterrows()]
        except Exception:
            return []
    
    def find_all(self) -> List[AgendaEvent]:
        """Implementa el puerto: buscar todos"""
        try:
            df = self._load_dataframe()
            return [AgendaEvent.from_dict(row) for _, row in df.iterrows()]
        except Exception:
            return []
    
    def delete(self, evento: str, fecha: str) -> bool:
        """Implementa el puerto: eliminar evento"""
        try:
            df = self._load_dataframe()
            initial_count = len(df)
            df = df[~((df['Evento'] == evento) & (df['Fecha'] == fecha))]
            
            if len(df) < initial_count:
                self._save_dataframe(df)
                return True
            return False
        except Exception:
            return False