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
        
        # Validación mínima (responsabilidad del configurador)
        if not api_key:
            raise ValueError("GEMINI_API_KEY es obligatoria")
        
        # Inyección de dependencias hexagonal:
        # 1. Puerto secundario (salida)
        repository_port = ExcelAgendaAdapter(agenda_file)
        
        # 2. Núcleo de aplicación
        agenda_service = AgendaService(repository_port)
        
        # 3. Puerto primario (entrada) - IA
        ai_agent_port = LangChainAgentAdapter(agenda_service, api_key)
        
        # 4. Puerto primario (entrada) - UI
        ui_adapter = StreamlitAdapter(ai_agent_port)
        
        return ui_adapter