@echo off
REM ========================================
REM REINICIAR REACT - VERSAO SIMPLES
REM Sem problemas de permissao!
REM ========================================

echo.
echo ============================================================
echo   REINICIANDO REACT DASHBOARD
echo ============================================================
echo.

REM Ir para pasta correta
cd /d "%~dp0auronex-dashboard"

echo [1/3] Parando processos Node.js...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/3] Deletando cache Next.js...
if exist .next rmdir /s /q .next
timeout /t 1 /nobreak >nul

echo [3/3] Iniciando React...
echo.
echo ============================================================
echo   URL: http://localhost:3000
echo   Aguarde ~20 segundos para compilar
echo ============================================================
echo.

npm run dev

pause

