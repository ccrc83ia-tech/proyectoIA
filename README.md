# Asistente de Agenda IA - LangChain

Asistente inteligente que utiliza **LangChain como framework principal** para gestionar una agenda simple en Excel.

## 🏠 Arquitectura del Proyecto

```
proyecto/
├── agenda_assistant/
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

## 🔄 Flujo de Datos

```
Usuario → Streamlit → LangChain Agent → Casos de Uso → Excel
```

### Componentes:
1. **Dominio**: Entidad `Evento`
2. **Aplicación**: `AgendaService` con casos de uso
3. **LangChain**: Framework principal - interpreta lenguaje natural
4. **Excel**: Persistencia de datos
5. **Streamlit**: Interfaz de usuario

## 🤖 LangChain como Framework Principal

- **Agente**: Interpreta solicitudes en lenguaje natural
- **Decisión**: Determina si agregar, consultar o eliminar eventos
- **Herramientas**: Operaciones sobre la agenda
- **Memoria**: Mantiene contexto de conversación (opcional)
- **Validación**: Formatos de entrada (opcional)

## 📈 Archivo Excel (agenda.xlsx)

| Columna | Formato | Descripción |
|---------|---------|-------------|
| Evento | Texto | Nombre del evento |
| Fecha | YYYY-MM-DD | Fecha del evento |
| Hora | HH:MM | Hora del evento |

## 🚀 Cómo Ejecutar

### Local
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar API Key
# Opción A: Crear .env con: GEMINI_API_KEY=tu_api_key
# Opción B: Variable de entorno: set GEMINI_API_KEY=tu_api_key
# Opción C: La aplicación te pedirá la key al iniciar

# 3. Ejecutar
streamlit run app_hexagonal.py
# O ejecutar directamente desde PyCharm/IDE
python app_hexagonal.py
```

### Docker (Opcional)
**Instalación en Windows:**
```powershell
# Opción 1: Docker Desktop (Recomendado)
# Descargar desde: https://www.docker.com/products/docker-desktop/
# Instalar y reiniciar el sistema

# Opción 2: Chocolatey
choco install docker-desktop

# Opción 3: Winget
winget install Docker.DockerDesktop
```

**Instalación en WSL (Windows Subsystem for Linux):**
```bash
# Instalar Docker en WSL
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Reiniciar WSL
exit
# Reabrir terminal WSL

# Iniciar servicio Docker
sudo service docker start
```

**Instalación en Ubuntu:**
```bash
# Instalar Docker
sudo apt update
sudo apt install docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Agregar usuario al grupo docker (opcional, evita usar sudo)
sudo usermod -aG docker $USER
# Reiniciar sesión después de este comando
```

**Generar imagen:**
```bash
# Verificar Docker
docker --version

# Construir imagen
docker build -t agenda-ai .

# Ejecutar contenedor
docker run -p 8501:8501 -e GEMINI_API_KEY=tu_key agenda-ai
```

**Acceder:** http://localhost:8501

## 💬 Ejemplos de Uso

- "Agregar reunión el 2024-01-15 a las 10:30"
- "¿Qué eventos tengo el 2024-01-15?"
- "Eliminar reunión del 2024-01-15"
- "Eliminar todos los eventos"
- "Exportar agenda"
- "Descargar mi agenda como Excel"

## ⚙️ Configuración

```env
GEMINI_API_KEY=tu_api_key_de_gemini
AGENDA_FILE=agenda.xlsx
COMPANY_NAME=Tu_Empresa
LOG_LEVEL=INFO
```

### GitHub Actions
Para CI/CD, configura el secreto `KEY_AUDIFARMA` en:
- Repository Settings → Secrets and variables → Actions → New repository secret
- Name: `KEY_AUDIFARMA`
- Value: Tu API key de Gemini

## ✅ Requisitos Cumplidos

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

### 🎆 Funcionalidades Adicionales:
- ✅ **Exportación a Excel**: Descargar agenda en formato Excel
- ✅ **Eliminación masiva**: Comando para eliminar todos los eventos
- ✅ **Confirmación de eliminación**: Verifica existencia antes de eliminar
- ✅ **Seguridad**: Protección XSS y sanitización de entradas
- ✅ **Ejecución flexible**: Desde terminal, IDE o input dinámico de API key
- ✅ **Logging**: Sistema de logs con archivos diarios