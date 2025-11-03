@echo off
title RoboTrader - Django (Sistema Original)
color 0E

echo ========================================
echo   ROBOTRADER - DJANGO (Original)
echo ========================================
echo Landing Page + Admin + Dashboard HTML
echo Aguarde enquanto inicio...
echo.

REM Matar processos antigos
taskkill /F /IM python.exe >nul 2>&1

timeout /t 3 /nobreak >nul

echo Iniciando componentes...
echo.

REM 1. Django
echo [1/4] Django (Waitress - porta 8000)...
start "Django Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd saas && waitress-serve --port=8000 saas.wsgi:application"

timeout /t 3 /nobreak >nul

REM 2. Celery Worker (usando Django celery)
echo [2/4] Celery Worker...
start "Celery Worker" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd saas && celery -A saas worker --loglevel=info --pool=solo"

timeout /t 3 /nobreak >nul

REM 3. Celery Beat
echo [3/4] Celery Beat...
start "Celery Beat" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd saas && celery -A saas beat --loglevel=info"

timeout /t 3 /nobreak >nul

REM 4. Streamlit (opcional)
echo [4/4] Streamlit Dashboard...
start "Dashboard" cmd /k "cd /d %~dp0 && venv\Scripts\activate && streamlit run dashboard_master.py --server.port=8501"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   SISTEMA DJANGO INICIADO!
echo ========================================
echo.
echo Acesse:
echo   Landing Page: http://localhost:8000
echo   Django Admin: http://localhost:8000/admin
echo   Dashboard: http://localhost:8000/dashboard
echo   API Keys: http://localhost:8000/api-keys
echo   Bots: http://localhost:8000/bots
echo.
echo   Streamlit: http://localhost:8501
echo.
echo IMPORTANTE: NAO FECHE as 4 janelas!
echo.
pause














