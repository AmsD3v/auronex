@echo off
title RoboTrader - Sistema Principal
color 0B

echo ========================================
echo   ROBOTRADER - INICIANDO SISTEMA
echo ========================================
echo.
echo Aguarde enquanto inicio todos componentes...
echo.

REM Matar processos antigos
taskkill /F /IM python.exe 2>nul
timeout /t 3 >nul

echo Iniciando componentes...
echo.

REM Django com Waitress
echo [1/4] Django (Waitress)...
start "Django" cmd /k "cd /d I:\Robo && venv\Scripts\activate && set PYTHONPATH=I:\Robo && cd saas && waitress-serve --port=8001 --host=127.0.0.1 saas.wsgi:application"
timeout /t 8 >nul

REM Celery Worker
echo [2/4] Celery Worker...
start "Celery Worker" cmd /k "cd /d I:\Robo && venv\Scripts\activate && set PYTHONPATH=I:\Robo && cd saas && celery -A saas worker --pool=solo --loglevel=info"
timeout /t 8 >nul

REM Celery Beat
echo [3/4] Celery Beat...
start "Celery Beat" cmd /k "cd /d I:\Robo && venv\Scripts\activate && set PYTHONPATH=I:\Robo && cd saas && celery -A saas beat --loglevel=info"
timeout /t 8 >nul

REM Dashboard
echo [4/4] Dashboard...
start "Dashboard" cmd /k "cd /d I:\Robo && venv\Scripts\activate && streamlit run dashboard_master.py --server.port 8501 --server.address 127.0.0.1"

echo.
echo ========================================
echo   AGUARDANDO INICIALIZACAO...
echo ========================================
echo.

timeout /t 30 >nul

echo.
echo ========================================
echo   SISTEMA INICIADO!
echo ========================================
echo.
echo Acesse:
echo   Dashboard: http://localhost:8501
echo   Django Admin: http://localhost:8001/admin
echo.
echo Bot configurado:
echo   - 10 simbolos
echo   - Filtro 0.1%% (ultra agressivo)
echo   - Waitress (servidor robusto)
echo.
echo Primeiro trade: 5-15 minutos
echo.
echo IMPORTANTE: NAO FECHE as 4 janelas!
echo.
pause


