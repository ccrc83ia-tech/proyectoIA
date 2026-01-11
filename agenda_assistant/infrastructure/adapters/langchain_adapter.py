"""Adaptador LangChain siguiendo estándares hexagonales."""
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from ..ports.service_ports import AIAgentPort, AgendaServicePort
import re
from datetime import datetime


class LangChainAgentAdapter(AIAgentPort):
    """Adaptador LangChain que respeta los principios hexagonales."""

    def __init__(self, agenda_service: AgendaServicePort, api_key: str, company_name: str = "Tu Empresa"):
        if not agenda_service:
            raise ValueError("agenda_service no puede ser None")
        if not api_key:
            raise ValueError("GEMINI_API_KEY es obligatoria")
        
        self.agenda_service = agenda_service
        self.company_name = company_name
        
        # Configurar LLM con LangChain
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0
        )
        
        # Prompt template
        self.prompt = PromptTemplate(
            input_variables=["query", "history", "current_date", "user_name", "company_name"],
            template="""
Eres un asistente de agenda inteligente de {company_name}.

Fecha actual: {current_date}
Usuario conocido: {user_name}
Historial reciente: {history}

IMPORTANTE: Si el usuario dice su nombre (ej: "hola, soy camilo"), responde con: NOMBRE|nombre_del_usuario

Si ya conoces al usuario, analiza su consulta y determina qué acción realizar:
1. Para crear eventos: "AGREGAR|descripcion_evento|YYYY-MM-DD|HH:MM"
2. Para consultar fecha específica: "CONSULTAR|YYYY-MM-DD"
3. Para ver todos los eventos: "LISTAR"
4. Para eliminar: "ELIMINAR|nombre_evento|YYYY-MM-DD"

Ejemplos de interpretación:
- "crear evento mañana 9 am" → AGREGAR|evento|2024-01-16|09:00
- "agendar reunión mañana 9" → AGREGAR|reunión|2024-01-16|09:00
- "ver eventos" o "listar" → LISTAR
- "qué tengo mañana" → CONSULTAR|2024-01-16

Calcula fechas relativas basado en {current_date}:
- "hoy" = {current_date}
- "mañana" = día siguiente
- "pasado mañana" = dos días después

Consulta del usuario: {query}

Responde SOLO con el formato de acción correspondiente:
"""
        )
        
        # Memoria simple para conversación
        self.conversation_history = []
        self.user_name = None

    def _validate_date(self, fecha: str) -> bool:
        """Valida formato de fecha."""
        try:
            from datetime import datetime
            datetime.fromisoformat(fecha)
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
                return f"¡Hola {self.user_name}! Es un placer conocerte. Soy tu asistente de agenda de {self.company_name} y estoy aquí para ayudarte con la gestión de tu agenda personal."
            
            # Si no conocemos el nombre, preguntar primero
            if not self.user_name:
                return f"¡Hola! Soy tu asistente de agenda de {self.company_name}. Antes de ayudarte, ¿podrías decirme tu nombre?"
            
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
            # Detectar si el usuario dice su nombre directamente
            query_lower = query.lower().strip()
            
            # Si no tenemos nombre y el usuario responde con solo una palabra (probable nombre)
            if not self.user_name:
                # Casos: "camilo", "soy camilo", "me llamo camilo", "hola soy camilo"
                if len(query.strip().split()) == 1 and query.strip().isalpha():
                    # Solo una palabra alfabética = nombre
                    self.user_name = query.strip().capitalize()
                    return f"¡Hola {self.user_name}! Es un placer conocerte. Soy tu asistente de agenda de {self.company_name} y estoy aquí para ayudarte con la gestión de tu agenda personal."
                elif "soy" in query_lower or "me llamo" in query_lower:
                    # Extraer nombre de frases como "hola, soy camilo" o "me llamo juan"
                    words = query_lower.replace(",", "").split()
                    if "soy" in words:
                        idx = words.index("soy")
                        if idx + 1 < len(words):
                            self.user_name = words[idx + 1].capitalize()
                    elif "llamo" in words:
                        idx = words.index("llamo")
                        if idx + 1 < len(words):
                            self.user_name = words[idx + 1].capitalize()
                    
                    if self.user_name:
                        return f"¡Hola {self.user_name}! Es un placer conocerte. Soy tu asistente de agenda de {self.company_name} y estoy aquí para ayudarte con la gestión de tu agenda personal."
            
            # Agregar a historial (memoria de conversación)
            self.conversation_history.append(f"Usuario: {query}")
            
            # Mantener solo últimas 6 interacciones para el contexto
            if len(self.conversation_history) > 12:
                self.conversation_history = self.conversation_history[-12:]
            
            # Obtener fecha actual
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Procesar con LangChain solo si tenemos nombre
            if self.user_name:
                history = "\n".join(self.conversation_history[-6:])  # Solo últimas 6 para contexto
                formatted_prompt = self.prompt.format(
                    query=query, 
                    history=history,
                    current_date=current_date,
                    user_name=self.user_name,
                    company_name=self.company_name
                )
                
                # Invocar LLM con LangChain
                result = self.llm.invoke(formatted_prompt)
                action = result.content.strip()
                
                # Ejecutar acción
                response = self._execute_action(action)
            else:
                # Si no tenemos nombre, pedirlo
                response = f"¡Hola! Soy tu asistente de agenda de {self.company_name}. Antes de ayudarte, ¿podrías decirme tu nombre?"
            
            # Agregar respuesta al historial
            self.conversation_history.append(f"Asistente: {response}")
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.conversation_history.append(f"Asistente: {error_msg}")
            return error_msg