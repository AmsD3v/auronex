@echo off
REM ========================================
REM REINICIAR TUDO LIMPO - SEM CACHE
REM ========================================

echo.
echo ============================================================
echo   REINICIANDO SISTEMA COMPLETO
echo   Limpando cache e iniciando tudo limpo
echo ============================================================
echo.

REM Parar tudo
echo [1/5] Parando processos...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Limpar cache React
echo [2/5] Limpando cache React...
cd /d I:\Robo\auronex-dashboard
if exist .next rmdir /s /q .next
timeout /t 1 /nobreak >nul

REM Atualizar .env.local
echo [3/5] Configurando .env.local...
echo NEXT_PUBLIC_API_URL=http://localhost:8001 > .env.local
echo NODE_ENV=development >> .env.local
echo.

REM Iniciar Backend em nova janela
echo [4/5] Iniciando Backend FastAPI...
cd /d I:\Robo
start "Backend FastAPI" cmd /k "venv\Scripts\activate && uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"
timeout /t 3 /nobreak >nul

REM Iniciar React em nova janela
echo [5/5] Iniciando Dashboard React...
cd /d I:\Robo\auronex-dashboard
start "Dashboard React" cmd /k "npm run dev"

echo.
echo ============================================================
echo   SISTEMA INICIANDO...
echo.
echo   Aguarde ~30 segundos
echo.
echo   Backend: http://localhost:8001
echo   Dashboard: http://localhost:8501
echo.
echo   Acesse: http://localhost:8501
echo ============================================================
echo.

timeout /t 5
start http://localhost:8501

pause

