@echo off
title Bot Controller APENAS
cd /d I:\Robo
call venv\Scripts\activate
echo ============================================================
echo   BOT CONTROLLER RODANDO
echo   SEM FastAPI (separado!)
echo   Gerencia bots automaticamente
echo ============================================================
echo.
python -m bot.bot_controller
pause


