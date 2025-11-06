@echo off
REM ========================================
REM INICIAR REACT - VERSAO ULTRA SIMPLES
REM ========================================

echo.
echo ============================================================
echo   INICIANDO DASHBOARD REACT
echo ============================================================
echo.

REM Ir para pasta
cd /d I:\Robo\auronex-dashboard

echo [1/2] Parando Node.js anteriores...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/2] Iniciando React...
echo.
echo ============================================================
echo   Aguarde ~30 segundos para compilar
echo   URL: http://localhost:8501
echo ============================================================
echo.

npm run dev

