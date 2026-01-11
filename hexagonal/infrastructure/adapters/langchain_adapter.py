"""Adaptador LangChain siguiendo estándares hexagonales."""
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from ..ports.service_ports import AIAgentPort, AgendaServicePort
import re
from datetime import datetime


class LangChainAgentAdapter(AIAgentPort):
    """Adaptador LangChain que respeta los principios hexagonales."""

    def __init__(self, agenda_service: AgendaServicePort, api_key: str):
        if not api_key:
            raise ValueError("GEMINI_API_KEY es obligatoria")
        
        self.agenda_service = agenda_service
        
        # Configurar LLM con LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0
        )
        
        # Prompt template
        self.prompt = PromptTemplate(
            input_variables=["query", "history", "current_date", "user_name"],
            template="""
Eres un asistente de agenda inteligente de Audifarma.

Fecha actual: {current_date}
Usuario: {user_name}
Historial: {history}

Analiza la consulta del usuario y determina qué acción realizar:
1. AGREGAR evento: "AGREGAR|nombre|YYYY-MM-DD|HH:MM"
2. CONSULTAR eventos: "CONSULTAR|YYYY-MM-DD"
3. ELIMINAR evento: "ELIMINAR|nombre|YYYY-MM-DD"
4. LISTAR todos: "LISTAR"
5. NOMBRE usuario: "NOMBRE|nombre_usuario"

Si el usuario dice "mañana", "hoy", "pasado mañana", calcula la fecha correcta basándote en la fecha actual.
Si no conoces el nombre del usuario, pregunta por él primero.
Usa el nombre del usuario en tus respuestas para personalizar la experiencia.
Recuerda que trabajas para Audifarma y ayudas con la gestión de agenda.

Consulta: {query}

Responde SOLO con el formato de acción correspondiente:
"""
        )
        
        # Memoria simple para conversación
        self.conversation_history = []
        self.user_name = None

    def _validate_date(self, fecha: str) -> bool:
        """Valida formato de fecha."""
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _validate_time(self, hora: str) -> bool:
        """Valida formato de hora."""
        pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
        return bool(re.match(pattern, hora))

    def _execute_action(self, action: str) -> str:
        """Ejecuta la acción determinada."""
        try:
            parts = action.strip().split('|')
            command = parts[0].upper()
            
            if command == "NOMBRE" and len(parts) == 2:
                _, nombre = parts
                self.user_name = nombre.strip()
                return f"¡Hola {self.user_name}! Es un placer conocerte. Soy tu asistente de agenda de Audifarma y estoy aquí para ayudarte con la gestión de tu agenda personal."
            
            # Si no conocemos el nombre, preguntar primero
            if not self.user_name:
                return "¡Hola! Soy tu asistente de agenda de Audifarma. Antes de ayudarte, ¿podrías decirme tu nombre?"
            
            if command == "AGREGAR" and len(parts) == 4:
                _, evento, fecha, hora = parts
                if not evento.strip():
                    return f"{self.user_name}, el nombre del evento no puede estar vacío"
                if not self._validate_date(fecha):
                    return f"{self.user_name}, la fecha '{fecha}' no es válida. Usa formato YYYY-MM-DD"
                if not self._validate_time(hora):
                    return f"{self.user_name}, la hora '{hora}' no es válida. Usa formato HH:MM"
                result = self.agenda_service.create_event(evento.strip(), fecha, hora)
                return f"{self.user_name}, {result}"
            
            elif command == "CONSULTAR" and len(parts) == 2:
                _, fecha = parts
                if not self._validate_date(fecha):
                    return f"{self.user_name}, la fecha '{fecha}' no es válida. Usa formato YYYY-MM-DD"
                result = self.agenda_service.get_events_by_date(fecha)
                return f"{self.user_name}, {result}"
            
            elif command == "ELIMINAR" and len(parts) == 3:
                _, evento, fecha = parts
                if not evento.strip():
                    return f"{self.user_name}, el nombre del evento no puede estar vacío"
                if not self._validate_date(fecha):
                    return f"{self.user_name}, la fecha '{fecha}' no es válida. Usa formato YYYY-MM-DD"
                result = self.agenda_service.delete_event(evento.strip(), fecha)
                return f"{self.user_name}, {result}"
            
            elif command == "LISTAR":
                result = self.agenda_service.get_all_events()
                return f"{self.user_name}, {result}"
            
            else:
                return f"¡Hola {self.user_name}! Puedo ayudarte con tu agenda. Ejemplos:\n- 'Agregar reunión mañana 10:30'\n- '¿Qué tengo el 2024-01-15?'\n- 'Eliminar reunión'"
                
        except Exception as e:
            user_prefix = f"{self.user_name}, " if self.user_name else ""
            return f"{user_prefix}❌ Error: {str(e)}"

    def process_natural_language(self, query: str) -> str:
        """Implementa el puerto AIAgentPort usando LangChain."""
        try:
            # Agregar a historial (memoria de conversación)
            self.conversation_history.append(f"Usuario: {query}")
            
            # Mantener solo últimas 10 interacciones
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            # Obtener fecha actual
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Procesar con LangChain
            history = "\n".join(self.conversation_history[-6:])  
            formatted_prompt = self.prompt.format(
                query=query, 
                history=history,
                current_date=current_date,
                user_name=self.user_name or "Usuario desconocido"
            )
            
            # Invocar LLM con LangChain
            result = self.llm.invoke(formatted_prompt)
            action = result.content.strip()
            
            # Ejecutar acción
            response = self._execute_action(action)
            
            # Agregar respuesta al historial
            self.conversation_history.append(f"Asistente: {response}")
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.conversation_history.append(f"Asistente: {error_msg}")
            return error_msg