@echo off
echo ===================================
echo   AURONEX - SISTEMA COMPLETO
echo   Backend FastAPI + Frontend React
echo ===================================
echo.

REM Verificar se venv existe
if not exist "venv\Scripts\activate.bat" (
    echo [ERRO] Ambiente virtual Python nao encontrado!
    echo.
    echo Crie o venv primeiro:
    echo python -m venv venv
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Verificar se node_modules existe
if not exist "auronex-dashboard\node_modules" (
    echo [AVISO] Dependencias React nao instaladas!
    echo [INFO] Instalando...
    echo.
    cd auronex-dashboard
    call npm install
    cd ..
    echo.
)

echo [OK] Tudo pronto! Iniciando sistema...
echo.
echo ===================================
echo   INICIANDO 2 TERMINAIS
echo ===================================
echo.
echo Terminal 1: Backend FastAPI (porta 8001)
echo Terminal 2: Frontend React (porta 3000)
echo.
echo Aguarde ambos iniciarem (~15 segundos)
echo.

REM Iniciar Backend em nova janela
start "Auronex - Backend FastAPI" cmd /k "cd /d %CD% && call venv\Scripts\activate.bat && uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"

REM Aguardar 3 segundos
timeout /t 3 /nobreak >nul

REM Iniciar Frontend em nova janela
start "Auronex - Frontend React" cmd /k "cd /d %CD%\auronex-dashboard && npm run dev"

echo.
echo ===================================
echo   SISTEMA INICIADO!
echo ===================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo [OK] Abra o navegador e acesse:
echo      http://localhost:3000
echo.
echo Para PARAR o sistema:
echo   - Feche as 2 janelas que abriram
echo   - Ou pressione Ctrl+C em cada uma
echo.

pause

