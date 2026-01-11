# Asistente de Agenda IA - LangChain

Asistente inteligente que utiliza **LangChain como framework principal** para gestionar una agenda simple en Excel.

## Arquitectura del Proyecto

```
prueba/
├── hexagonal/
│   ├── domain/
│   │   └── entities.py           # Entidades de negocio
│   ├── application/
│   │   └── agenda_service.py     # Casos de uso
│   └── infrastructure/
│       ├── ports/                # Interfaces
│       └── adapters/             # Implementaciones
├── app_hexagonal.py              # Aplicación principal
├── requirements.txt              # Dependencias
├── .env                         # Configuración
├── Dockerfile                   # Containerización (opcional)
└── README.md                    # Documentación
```

## Flujo de Datos

```
Usuario → Streamlit → LangChain Agent → Casos de Uso → Excel
```

### Componentes:
1. **Dominio**: Entidad `Evento`
2. **Aplicación**: `AgendaService` con casos de uso
3. **LangChain**: Framework principal - interpreta lenguaje natural
4. **Excel**: Persistencia de datos
5. **Streamlit**: Interfaz de usuario

## LangChain como Framework Principal

- **Agente**: Interpreta solicitudes en lenguaje natural
- **Decisión**: Determina si agregar, consultar o eliminar eventos
- **Herramientas**: Operaciones sobre la agenda
- **Memoria**: Mantiene contexto de conversación (opcional)
- **Validación**: Formatos de entrada (opcional)

## Archivo Excel (agenda.xlsx)

| Columna | Formato | Descripción |
|---------|---------|-------------|
| Evento | Texto | Nombre del evento |
| Fecha | YYYY-MM-DD | Fecha del evento |
| Hora | HH:MM | Hora del evento |

## Cómo Ejecutar

### Local
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar API Key
# Crear .env con: GEMINI_API_KEY=tu_api_key

# 3. Ejecutar
streamlit run app_hexagonal.py
```

### Docker (Opcional)
```bash
docker build -t agenda-ai .
docker run -p 8501:8501 -e GEMINI_API_KEY=tu_key agenda-ai
```

## Ejemplos de Uso

- "Agregar reunión el 2024-01-15 a las 10:30"
- "¿Qué eventos tengo el 2024-01-15?"
- "Eliminar reunión del 2024-01-15"

## Configuración

```env
GEMINI_API_KEY=tu_api_key_de_gemini
AGENDA_FILE=agenda.xlsx
```

## Requisitos Cumplidos

### Obligatorios:
- ✅ **LangChain**: Framework principal de orquestación
- ✅ **Streamlit**: Interfaz de usuario
- ✅ **Excel**: Persistencia con columnas requeridas
- ✅ **Lenguaje Natural**: Interpretación de comandos
- ✅ **Operaciones**: Agregar, consultar, eliminar eventos
- ✅ **Código Limpio**: Modular y documentado
- ✅ **README**: Arquitectura y ejecución explicados

### Opcionales:
- ✅ **Memoria de conversación**: LangChain mantiene contexto
- ✅ **Validación de entradas**: Formatos de fecha y hora
- ✅ **Containerización**: Docker incluido