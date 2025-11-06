@echo off
REM ========================================
REM FORCAR REINICIO COMPLETO DO REACT
REM Mata processos, limpa cache, reinicia
REM ========================================

echo.
echo ============================================================
echo   FORCANDO REINICIO TOTAL DO REACT DASHBOARD
echo ============================================================
echo.

REM 1. Matar TODOS os processos Node
echo [1/5] Matando processos Node.js...
taskkill /F /IM node.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM 2. Deletar cache Next.js
echo [2/5] Deletando cache Next.js...
cd auronex-dashboard
if exist .next rmdir /s /q .next
if exist node_modules\.cache rmdir /s /q node_modules\.cache
timeout /t 1 /nobreak >nul

REM 3. Verificar se node_modules existe
echo [3/5] Verificando dependencias...
if not exist node_modules (
    echo    Instalando dependencias...
    call npm install
)

REM 4. Limpar cache npm
echo [4/5] Limpando cache npm...
call npm cache clean --force >nul 2>&1

REM 5. Iniciar React limpo
echo [5/5] Iniciando React Dashboard...
echo.
echo ============================================================
echo   DASHBOARD INICIANDO...
echo   Aguarde ~20 segundos
echo   URL: http://localhost:3000
echo ============================================================
echo.

call npm run dev

pause

