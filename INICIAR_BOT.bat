@echo off
chcp 65001 >nul
title Auronex - FastAPI com Bot
color 0A

echo ========================================
echo   AURONEX - FASTAPI + BOT CONTROLLER
echo ========================================
echo.
echo Iniciando FastAPI + Bot Controller
echo.
echo ⚠️  Bot Controller ATIVO
echo    Gerencia TODOS os bots automaticamente
echo.
echo ========================================
echo.

cd /d I:\Robo

start "FastAPI + Bot Controller" powershell -NoExit -Command "cd I:\Robo; Write-Host '========================================' -ForegroundColor Green; Write-Host '  FASTAPI + BOT CONTROLLER' -ForegroundColor Green; Write-Host '========================================' -ForegroundColor Green; Write-Host ''; Write-Host 'Bot Controller: ATIVO' -ForegroundColor Green; Write-Host 'Gerencia bots automaticamente!' -ForegroundColor Green; Write-Host ''; I:\Robo\venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"

timeout /t 10 /nobreak >nul

echo.
echo ✅ FastAPI + Bot iniciado!
echo.
echo 🌐 Acesse: http://localhost:8001/
echo 🤖 Bots sendo gerenciados automaticamente!
echo.

pause

