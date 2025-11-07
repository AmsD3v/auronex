@echo off
title FastAPI APENAS (8001)
cd /d I:\Robo
call venv\Scripts\activate
echo ============================================================
echo   FASTAPI RODANDO - PORTA 8001
echo   SEM Bot Controller (separado!)
echo ============================================================
echo.
uvicorn fastapi_app.main:app --port 8001 --reload
pause



