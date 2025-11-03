@echo off
REM ========================================
REM ROBOTRADER - VERSAO SIMPLES (SEM LOOP!)
REM ========================================

echo ========================================
echo   ROBOTRADER - Iniciando (Simples)
echo ========================================
echo.

cd /d I:\Robo

REM Matar processos antigos
echo [1/3] Limpando processos...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM streamlit.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando Django...
start "RoboTrader Django" cmd /k "cd /d I:\Robo\saas && ..\venv\Scripts\activate && python manage.py runserver 8001"

echo [3/3] Aguardando Django (10s) e iniciando Streamlit...
timeout /t 10 /nobreak >nul

start "RoboTrader Streamlit" cmd /k "cd /d I:\Robo && venv\Scripts\activate && streamlit run dashboard_master.py --server.port 8501"

echo.
echo ========================================
echo   SISTEMA INICIADO!
echo ========================================
echo.
echo Django:    http://localhost:8001
echo Streamlit: http://localhost:8501
echo.
echo Mantenha as 2 janelas abertas!
echo Para parar: Feche as janelas
echo.
pause

