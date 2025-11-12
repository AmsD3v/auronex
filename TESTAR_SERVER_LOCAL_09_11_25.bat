@echo off
REM ====================================
REM TESTAR SERVIDOR LOCAL - 09/11/2025
REM 3 Janelas: FastAPI + React + Bot Controller
REM ====================================

echo.
echo ============================================================
echo   INICIANDO SISTEMA LOCAL - 09/11/2025
echo   3 Janelas: FastAPI + React + Bot Controller
echo ============================================================
echo.

cd /d I:\Robo

REM Janela 1: FastAPI (porta 8001)
echo [1/3] Iniciando FastAPI...
start "1-FastAPI-8001" cmd /k "title FastAPI (8001) && cd /d I:\Robo && venv\Scripts\activate && echo ============================================================ && echo   FASTAPI RODANDO - PORTA 8001 && echo ============================================================ && echo. && uvicorn fastapi_app.main:app --port 8001 --reload"

timeout /t 5

REM Janela 2: Dashboard React (porta 8501) - MODO DEV
echo [2/3] Iniciando Dashboard React (DEV MODE)...
start "2-Dashboard-React-8501" cmd /k "title Dashboard React DEV (8501) && cd /d I:\Robo\auronex-dashboard && echo ============================================================ && echo   DASHBOARD REACT - MODO DEV (HOT RELOAD) && echo   Chama APIs: http://localhost:8001 && echo ============================================================ && echo. && npm run dev"

timeout /t 3

REM Janela 3: Bot Controller (opcional)
echo [3/3] Iniciando Bot Controller...
start "3-Bot-Controller" cmd /k "title Bot Controller && cd /d I:\Robo && venv\Scripts\activate && echo ============================================================ && echo   BOT CONTROLLER && echo   Gerencia bots automaticamente && echo ============================================================ && echo. && python -m bot.bot_controller"

echo.
echo ============================================================
echo   SISTEMA INICIADO!
echo ============================================================
echo.
echo   URLs:
echo   - FastAPI: http://localhost:8001
echo   - Dashboard: http://localhost:8501
echo   - Admin: http://localhost:8001/admin/
echo.
echo   Feche as 3 janelas CMD para parar
echo ============================================================
echo.

pause

