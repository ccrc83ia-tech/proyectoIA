"""Aplicación principal del asistente de agenda."""
import sys
import os
import streamlit as st

# Configurar página ANTES que cualquier otra cosa de Streamlit
st.set_page_config(
    page_title="Asistente de Agenda IA",
    page_icon="📅",
    layout="wide"
)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agenda_assistant.infrastructure.hexagonal_configurator import HexagonalConfigurator
from agenda_assistant.infrastructure.logging_config import setup_logging

# Configurar logging
logger = setup_logging()


def main():
    """Punto de entrada principal."""
    try:
        logger.info("Iniciando aplicación Asistente de Agenda IA")
        ui_adapter = HexagonalConfigurator.wire_dependencies()
        ui_adapter.render_ui()
        
    except ValueError as e:
        logger.error(f"Error de configuración: {str(e)}")
        st.error(f"Error de configuración: {str(e)}")
        st.info("Configura GEMINI_API_KEY en el archivo .env")
        st.stop()
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        st.error(f"Error: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()