"""Aplicación principal del asistente de agenda."""
import sys
import os
import streamlit as st

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agenda_assistant.infrastructure.hexagonal_configurator import HexagonalConfigurator


def main():
    """Punto de entrada principal."""
    try:
        ui_adapter = HexagonalConfigurator.wire_dependencies()
        ui_adapter.render_ui()
        
    except ValueError as e:
        st.error(f"Error de configuración: {str(e)}")
        st.info("Configura GEMINI_API_KEY en el archivo .env")
        st.stop()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()


if __name__ == "__main__":
    main()