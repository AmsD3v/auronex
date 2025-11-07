@echo off
REM ====================================
REM TESTE LOCAL - 3 JANELAS SEPARADAS
REM FastAPI | Dashboard React | Bot Controller
REM ====================================

echo.
echo ============================================================
echo   INICIANDO SISTEMA DE TESTE
echo   3 Janelas: FastAPI + React + Bot Controller
echo ============================================================
echo.

cd /d I:\Robo

REM Janela 1: FastAPI APENAS (porta 8001)
echo [1/3] Iniciando FastAPI...
start "1-FastAPI" cmd /k "title FastAPI (8001) && cd /d I:\Robo && venv\Scripts\activate && echo ============================================================ && echo   FASTAPI RODANDO - PORTA 8001 && echo ============================================================ && echo. && uvicorn fastapi_app.main:app --port 8001 --reload"

timeout /t 5

REM Janela 2: Dashboard React APENAS (porta 8501)
echo [2/3] Iniciando Dashboard React...
start "2-Dashboard-React" cmd /k "title Dashboard React (8501) && cd /d I:\Robo\auronex-dashboard && echo ============================================================ && echo   DASHBOARD REACT - PORTA 8501 && echo ============================================================ && echo. && npm run dev"

timeout /t 3

REM Janela 3: Bot Controller APENAS
echo [3/3] Iniciando Bot Controller...
start "3-Bot-Controller" cmd /k "title Bot Controller && cd /d I:\Robo && venv\Scripts\activate && echo ============================================================ && echo   BOT CONTROLLER RODANDO && echo   Gerencia bots automaticamente && echo ============================================================ && echo. && python -m bot.bot_controller"

echo.
echo ============================================================
echo   ✅ SISTEMA INICIADO!
echo   3 Janelas CMD abertas:
echo.
echo   1. FastAPI (porta 8001)
echo   2. Dashboard React (porta 8501)  
echo   3. Bot Controller (background)
echo.
echo   URLs:
echo   - FastAPI: http://localhost:8001
echo   - Dashboard: http://localhost:8501
echo.
echo   Feche as 3 janelas CMD para parar tudo
echo ============================================================
echo.

pause

