@echo off
REM ========================================
REM DIAGNOSTICAR POR QUE REACT NAO RODA
REM ========================================

echo.
echo ============================================================
echo   DIAGNOSTICANDO REACT DASHBOARD
echo ============================================================
echo.

REM 1. Verificar se Node.js está instalado
echo [1/6] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ Node.js NAO instalado!
    echo    Instale: https://nodejs.org/
    pause
    exit /b 1
) else (
    node --version
    echo    ✅ Node.js OK
)
echo.

REM 2. Verificar se npm está instalado
echo [2/6] Verificando npm...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo    ❌ npm NAO instalado!
    pause
    exit /b 1
) else (
    npm --version
    echo    ✅ npm OK
)
echo.

REM 3. Verificar se pasta existe
echo [3/6] Verificando pasta auronex-dashboard...
cd /d "%~dp0auronex-dashboard" 2>nul
if %errorlevel% neq 0 (
    echo    ❌ Pasta auronex-dashboard NAO encontrada!
    echo    Localizacao esperada: %~dp0auronex-dashboard
    pause
    exit /b 1
) else (
    echo    ✅ Pasta encontrada
    cd
)
echo.

REM 4. Verificar package.json
echo [4/6] Verificando package.json...
if not exist package.json (
    echo    ❌ package.json NAO encontrado!
    pause
    exit /b 1
) else (
    echo    ✅ package.json OK
)
echo.

REM 5. Verificar node_modules
echo [5/6] Verificando node_modules...
if not exist node_modules (
    echo    ❌ node_modules NAO encontrado!
    echo    Executando npm install...
    call npm install
) else (
    echo    ✅ node_modules OK
)
echo.

REM 6. Verificar porta 3000
echo [6/6] Verificando porta 3000...
netstat -ano | findstr ":3000" >nul 2>&1
if %errorlevel% equ 0 (
    echo    ⚠️  Porta 3000 JA esta em uso!
    echo.
    echo    Processos na porta 3000:
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000"') do (
        echo       PID: %%a
        tasklist /FI "PID eq %%a" /FO TABLE
    )
    echo.
    echo    SOLUCAO:
    echo    1. Feche o processo acima
    echo    2. OU execute: taskkill /F /PID [numero_do_pid]
) else (
    echo    ✅ Porta 3000 livre
)
echo.

echo ============================================================
echo   DIAGNOSTICO CONCLUIDO
echo ============================================================
echo.
echo PROXIMO PASSO:
echo   1. Se tudo OK: npm run dev
echo   2. Se porta em uso: Matar processo
echo   3. Se node_modules faltando: npm install (ja executado)
echo.
pause

