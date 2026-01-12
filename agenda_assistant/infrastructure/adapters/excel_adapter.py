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
        except PermissionError as e:
            self.logger.error(f"Sin permisos para acceder al archivo: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error al cargar archivo Excel: {e}")
            raise
    
    def _save_dataframe(self, df: pd.DataFrame):
        """Guarda el DataFrame en Excel"""
        try:
            df.to_excel(self.file_path, index=False)
        except PermissionError as e:
            self.logger.error(f"Sin permisos para escribir archivo: {e}")
            raise
        except OSError as e:
            self.logger.error(f"Error del sistema al escribir archivo: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error inesperado al guardar Excel: {e}")
            raise
    
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
    
    def delete_all(self) -> bool:
        """Implementa el puerto: eliminar todos los eventos"""
        try:
            df = self._load_dataframe()
            initial_count = len(df)
            
            if initial_count == 0:
                return False  # No hay eventos para eliminar
            
            # Crear DataFrame vacío con las mismas columnas
            empty_df = pd.DataFrame(columns=['Evento', 'Fecha', 'Hora'])
            self._save_dataframe(empty_df)
            return True
            
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"Error de archivo al eliminar todos: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado al eliminar todos: {e}")
            return False
    
    def export_to_excel(self, export_path: str) -> bool:
        """Exporta la agenda a un archivo Excel específico"""
        try:
            df = self._load_dataframe()
            
            if df.empty:
                return False  # No hay eventos para exportar
            
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(export_path), exist_ok=True)
            
            # Exportar con formato mejorado
            with pd.ExcelWriter(export_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Agenda', index=False)
                
                # Obtener la hoja para formatear
                worksheet = writer.sheets['Agenda']
                
                # Ajustar ancho de columnas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            return True
            
        except (FileNotFoundError, PermissionError) as e:
            self.logger.error(f"Error de archivo al exportar: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error inesperado al exportar: {e}")
            return False