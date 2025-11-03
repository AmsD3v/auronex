@echo off
title RoboTrader - Sistema Completo (Django + FastAPI)
color 0A

echo ========================================
echo   ROBOTRADER - SISTEMA COMPLETO
echo ========================================
echo Django (porta 8000) + FastAPI (porta 8001)
echo Aguarde enquanto inicio...
echo.

REM Matar processos antigos
taskkill /F /IM python.exe >nul 2>&1

timeout /t 3 /nobreak >nul

echo Iniciando componentes...
echo.

REM 1. Django (porta 8000)
echo [1/5] Django (Waitress - porta 8000)...
start "Django Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate && cd saas && waitress-serve --port=8000 saas.wsgi:application"

timeout /t 3 /nobreak >nul

REM 2. FastAPI (porta 8001)
echo [2/5] FastAPI (Uvicorn - porta 8001)...
start "FastAPI" cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"

timeout /t 3 /nobreak >nul

REM 3. Celery Worker
echo [3/5] Celery Worker...
start "Celery Worker" cmd /k "cd /d %~dp0 && venv\Scripts\activate && celery -A fastapi_app.celery_fastapi worker --loglevel=info --pool=solo"

timeout /t 3 /nobreak >nul

REM 4. Celery Beat
echo [4/5] Celery Beat...
start "Celery Beat" cmd /k "cd /d %~dp0 && venv\Scripts\activate && celery -A fastapi_app.celery_fastapi beat --loglevel=info"

timeout /t 3 /nobreak >nul

REM 5. Streamlit Dashboard
echo [5/5] Streamlit Dashboard (porta 8501)...
start "Dashboard" cmd /k "cd /d %~dp0 && venv\Scripts\activate && streamlit run dashboard_master.py --server.port=8501"

timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   SISTEMA COMPLETO INICIADO!
echo ========================================
echo.
echo Acesse:
echo   Landing Page: http://localhost:8000
echo   Django Admin: http://localhost:8000/admin
echo   Dashboard HTML: http://localhost:8000/dashboard
echo.
echo   FastAPI Docs: http://localhost:8001/api/docs
echo   Streamlit: http://localhost:8501
echo.
echo IMPORTANTE: NAO FECHE as 5 janelas!
echo.
pause
