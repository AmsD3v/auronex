@echo off
REM Iniciar sistema - SIMPLES (sem echo complexo)
cd /d I:\Robo

REM FastAPI
start "FastAPI-8001" cmd /k "venv\Scripts\activate && uvicorn fastapi_app.main:app --port 8001 --reload"

timeout /t 5

REM React
start "React-8501" cmd /k "cd auronex-dashboard && npm run dev"

timeout /t 3

REM Bot Controller
start "Bot-Controller" cmd /k "venv\Scripts\activate && python -m bot.bot_controller"

echo.
echo Sistema iniciado! 3 janelas abertas.
echo FastAPI: http://localhost:8001
echo Dashboard: http://localhost:8501
echo.
pause
