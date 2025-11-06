@echo off
chcp 65001 >nul
title Auronex - FastAPI (Sem Bot)
color 0B

echo ========================================
echo   AURONEX - FASTAPI (SEM BOT)
echo ========================================
echo.
echo Iniciando apenas FastAPI na porta 8001
echo.
echo ⚠️  Bot Controller DESABILITADO
echo    Use INICIAR_BOT.bat para iniciar bot
echo.
echo ========================================
echo.

cd /d I:\Robo

start "FastAPI (Sem Bot)" powershell -NoExit -Command "cd I:\Robo; Write-Host '========================================' -ForegroundColor Cyan; Write-Host '  FASTAPI (SEM BOT CONTROLLER)' -ForegroundColor Cyan; Write-Host '========================================' -ForegroundColor Cyan; Write-Host ''; Write-Host 'Bot Controller: DESABILITADO' -ForegroundColor Yellow; Write-Host 'Para iniciar bot: INICIAR_BOT.bat' -ForegroundColor Yellow; Write-Host ''; $env:DISABLE_BOT_CONTROLLER='true'; I:\Robo\venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"

timeout /t 10 /nobreak >nul

echo.
echo ✅ FastAPI iniciado (sem bot)!
echo.
echo 🌐 Acesse: http://localhost:8001/
echo.

pause
