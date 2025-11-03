@echo off
REM ROBOTRADER - Inicia TUDO e mantém rodando automaticamente
REM Reinicia se cair!

echo ========================================
echo   ROBOTRADER - Iniciando com Monitor
echo ========================================
echo.

cd /d I:\Robo

REM Ativar venv
call venv\Scripts\activate.bat

REM Iniciar monitor (mantém Django e Streamlit sempre rodando)
python keep_alive.py

pause

