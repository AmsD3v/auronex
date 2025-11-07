@echo off
REM ====================================
REM AMBIENTE DE TESTE LOCAL
REM 3 Janelas: FastAPI + React + Bot
REM ====================================

cd /d I:\Robo

REM Janela 1: FastAPI (porta 8001)
start "Backend FastAPI" cmd /k "venv\Scripts\activate && uvicorn fastapi_app.main:app --port 8001 --reload"

timeout /t 3

REM Janela 2: Dashboard React (porta 8501)
start "Dashboard React" cmd /k "cd auronex-dashboard && npm run dev"

echo.
echo ============================================================
echo   SISTEMA DE TESTE INICIADO (SEM Bot Controller)
echo ============================================================
echo.
echo   FastAPI: http://localhost:8001
echo   Dashboard: http://localhost:8501
echo.
echo   Bot Controller: Inicie manualmente se necessario:
echo   python -m bot.bot_controller
echo.
echo   Feche as janelas para parar
echo ============================================================
echo.

pause

