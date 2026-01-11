"""Adaptador de interfaz de usuario con Streamlit."""
import streamlit as st
from ..ports.service_ports import AIAgentPort


class StreamlitAdapter:
    """Adaptador de entrada para interfaz web con Streamlit."""
    
    def __init__(self, ai_agent: AIAgentPort):
        # Guardar el agente en session_state para persistir memoria
        if 'ai_agent' not in st.session_state:
            st.session_state.ai_agent = ai_agent
        self.ai_agent = st.session_state.ai_agent
    
    def render_ui(self) -> None:
        """Renderiza la interfaz de usuario."""
        st.set_page_config(
            page_title="Asistente de Agenda IA",
            page_icon="📅",
            layout="wide"
        )
        
        st.title("Asistente de Agenda IA - Pragma")
        st.caption("Usando LangChain como framework principal")
        st.markdown("---")
        
        # Inicializar historial
        if 'messages' not in st.session_state:
            st.session_state.messages = [{
                "role": "assistant", 
                "content": "¡Hola! Soy tu asistente de agenda de Pragma. Antes de ayudarte, ¿podrías decirme tu nombre?"
            }]
        
        # Mostrar historial
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input del usuario
        if prompt := st.chat_input("¿Qué necesitas con tu agenda?"):
            # Mostrar mensaje del usuario
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Procesar con LangChain
            with st.chat_message("assistant"):
                with st.spinner("Procesando con LangChain..."):
                    response = self.ai_agent.process_natural_language(prompt)
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})