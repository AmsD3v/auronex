@echo off
echo ===================================
echo   AURONEX - DASHBOARD REACT
echo ===================================
echo.

REM Verificar se Node.js está instalado
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Node.js nao encontrado!
    echo.
    echo Instale Node.js em: https://nodejs.org/
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js instalado: 
node --version
echo.

REM Navegar para pasta do dashboard
cd auronex-dashboard

REM Verificar se node_modules existe
if not exist "node_modules" (
    echo [AVISO] Dependencias nao instaladas!
    echo [INFO] Instalando dependencias...
    echo.
    npm install
    echo.
)

echo ===================================
echo   INICIANDO DASHBOARD REACT
echo ===================================
echo.
echo URL: http://localhost:3000
echo.
echo Aguarde o dashboard iniciar...
echo (Pode demorar 10-20 segundos na primeira vez)
echo.

REM Iniciar dashboard
npm run dev

pause

