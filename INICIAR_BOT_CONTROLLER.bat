@echo off
REM Iniciar Bot Controller

cd /d I:\Robo

echo ============================================================
echo   BOT CONTROLLER - INICIANDO
echo ============================================================
echo.

venv\Scripts\activate && python -m bot.bot_controller

pause

