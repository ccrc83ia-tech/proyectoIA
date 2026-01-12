"""Configuración de logging para el proyecto."""
import logging
import os
from datetime import datetime


def setup_logging():
    """Configura el sistema de logging."""
    # Crear directorio de logs si no existe
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Nombre del archivo con fecha
    log_filename = f"agenda_assistant_{datetime.now().strftime('%Y%m%d')}.log"
    log_path = os.path.join(logs_dir, log_filename)
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()  # También mostrar en consola
        ]
    )
    
    return logging.getLogger(__name__)