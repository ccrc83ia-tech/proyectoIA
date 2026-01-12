"""Configurador de dependencias hexagonales."""
import os
from dotenv import load_dotenv
from .adapters.excel_adapter import ExcelAgendaAdapter
from .adapters.langchain_adapter import LangChainAgentAdapter
from .adapters.streamlit_adapter import StreamlitAdapter
from ..application.agenda_service import AgendaService


class HexagonalConfigurator:
    """Configurador puro de inyección de dependencias."""
    
    @staticmethod
    def wire_dependencies():
        """Conecta dependencias siguiendo principios hexagonales."""
        load_dotenv()
        
        # Obtener configuración
        agenda_file = os.getenv("AGENDA_FILE", "agenda.xlsx")
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Si la API key es una referencia a otra variable, resolverla
        if api_key and api_key.startswith("KEY_"):
            api_key = os.getenv(api_key)
        
        company_name = os.getenv("COMPANY_NAME", "Tu Empresa")
        
        # Si no hay API key en .env, usar input de Streamlit
        if not api_key:
            import streamlit as st
            api_key = st.text_input(
                "Ingresa tu GEMINI_API_KEY:", 
                type="password",
                help="Obtén tu API Key en: https://aistudio.google.com/app/api-keys"
            )
            if not api_key:
                st.warning("⚠️ Ingresa tu API Key para continuar")
                st.stop()
        
        # Inyección de dependencias hexagonal:
        # 1. Puerto secundario (salida)
        repository_port = ExcelAgendaAdapter(agenda_file)
        
        # 2. Núcleo de aplicación
        agenda_service = AgendaService(repository_port)
        
        # 3. Puerto primario (entrada) - IA
        ai_agent_port = LangChainAgentAdapter(agenda_service, api_key, company_name)
        
        # 4. Puerto primario (entrada) - UI
        ui_adapter = StreamlitAdapter(ai_agent_port)
        
        return ui_adapter