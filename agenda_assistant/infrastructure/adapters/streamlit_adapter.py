"""Adaptador de interfaz de usuario con Streamlit."""
import streamlit as st
import html
import logging
from ..ports.service_ports import AIAgentPort


class StreamlitAdapter:
    """Adaptador de entrada para interfaz web con Streamlit."""
    
    def __init__(self, ai_agent: AIAgentPort):
        # Guardar el agente en session_state para persistir memoria
        if 'ai_agent' not in st.session_state:
            st.session_state.ai_agent = ai_agent
        
        # Usar el agente del session_state o el pasado como parámetro
        self.ai_agent = st.session_state.ai_agent if 'ai_agent' in st.session_state else ai_agent
        self.logger = logging.getLogger(__name__)
    
    def _sanitize_input(self, text: str) -> str:
        """Sanitiza entrada del usuario para prevenir XSS."""
        if not text:
            return ""
        # Escapar solo caracteres peligrosos, no comillas simples
        return html.escape(text.strip(), quote=False)
    
    def render_ui(self) -> None:
        """Renderiza la interfaz de usuario."""
        st.title("Asistente de Agenda IA")
        st.caption("Usando LangChain como framework principal")
        st.markdown("---")
        
        # Inicializar historial
        if 'messages' not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant", 
                "content": "¡Hola! Soy tu asistente de agenda. Antes de ayudarte, ¿podrías decirme tu nombre?"
            }]
        
        # Mostrar historial
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Sanitizar contenido antes de mostrar
                safe_content = self._sanitize_input(message["content"])
                st.markdown(safe_content)  # Cambiar a markdown para renderizar correctamente
        
        # Input del usuario
        if prompt := st.chat_input("¿Qué necesitas con tu agenda?"):
            # Sanitizar entrada del usuario
            safe_prompt = self._sanitize_input(prompt)
            
            # Mostrar mensaje del usuario
            with st.chat_message("user"):
                st.text(safe_prompt)
            st.session_state.messages.append({"role": "user", "content": safe_prompt})
            
            # Procesar con LangChain
            with st.chat_message("assistant"):
                with st.spinner("Procesando con LangChain..."):
                    try:
                        response = self.ai_agent.process_natural_language(prompt)
                        safe_response = self._sanitize_input(response)
                        st.markdown(safe_response)  # Cambiar a markdown
                    except Exception as e:
                        self.logger.error(f"Error procesando solicitud: {e}")
                        error_msg = "❌ Error procesando tu solicitud. Intenta nuevamente."
                        st.error(error_msg)
                        safe_response = error_msg
            
            st.session_state.messages.append({"role": "assistant", "content": safe_response})