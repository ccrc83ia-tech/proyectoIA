@echo off
echo 🚀 Iniciando Asistente de Agenda IA...
echo.

REM Verificar si streamlit está instalado
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit no está instalado
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo ✅ Ejecutando aplicación...
streamlit run app_hexagonal.py

pause