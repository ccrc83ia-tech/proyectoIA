import pandas as pd
import os
import logging
from typing import List
from ..ports.agenda_repository_port import AgendaRepositoryPort
from ...domain.entities import AgendaEvent

class ExcelAgendaAdapter(AgendaRepositoryPort):
    """Adaptador de salida - Implementación para Excel"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Asegura que el archivo Excel existe"""
        if not os.path.exists(self.file_path):
            df = pd.DataFrame(columns=['Evento', 'Fecha', 'Hora'])
            df.to_excel(self.file_path, index=False)
    
    def _load_dataframe(self) -> pd.DataFrame:
        """Carga el DataFrame desde Excel"""
        try:
            return pd.read_excel(self.file_path)
        except FileNotFoundError:
            # Crear archivo si no existe
            df = pd.DataFrame(columns=['Evento', 'Fecha', 'Hora'])
            df.to_excel(self.file_path, index=False)
            return df
        except PermissionError as e:
            self.logger.error(f"Sin permisos para acceder al archivo: {e}")
            raise PermissionError(f"Sin permisos para acceder al archivo: {e}")
        except Exception as e:
            self.logger.error(f"Error al cargar archivo Excel: {e}")
            raise Exception(f"Error al cargar archivo Excel: {e}")
    
    def _save_dataframe(self, df: pd.DataFrame):
        """Guarda el DataFrame en Excel"""
        df.to_excel(self.file_path, index=False)
    
    def save(self, event: AgendaEvent) -> bool:
        """Implementa el puerto: guardar evento"""
        try:
            df = self._load_dataframe()
            # Usar loc para mejor rendimiento
            df.loc[len(df)] = event.to_dict()
            self._save_dataframe(df)
            return True
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"Error de archivo: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado al guardar: {e}")
            return False
    
    def find_by_date(self, fecha: str) -> List[AgendaEvent]:
        """Implementa el puerto: buscar por fecha"""
        try:
            df = self._load_dataframe()
            filtered_df = df[df['Fecha'] == fecha]
            return [AgendaEvent.from_dict(row) for _, row in filtered_df.iterrows()]
        except (FileNotFoundError, KeyError) as e:
            self.logger.error(f"Error al buscar por fecha: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error inesperado en búsqueda: {e}")
            return []
    
    def find_all(self) -> List[AgendaEvent]:
        """Implementa el puerto: buscar todos"""
        try:
            df = self._load_dataframe()
            return [AgendaEvent.from_dict(row) for _, row in df.iterrows()]
        except (FileNotFoundError, KeyError) as e:
            self.logger.error(f"Error al buscar todos los eventos: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error inesperado al obtener eventos: {e}")
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
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"Error de archivo al eliminar: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado al eliminar: {e}")
            return False