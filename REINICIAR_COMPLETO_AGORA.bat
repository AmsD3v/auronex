@echo off
REM ========================================
REM REINICIAR SISTEMA COMPLETO
REM ========================================

echo ======================================================================
echo   REINICIANDO SISTEMA AURONEX COMPLETO
echo ======================================================================
echo.

echo [1/3] Parando TODOS os processos...
echo.

REM Matar processos Python
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1

REM Matar processos Node
taskkill /F /IM node.exe >nul 2>&1

echo [OK] Processos parados
echo.

echo [2/3] Aguardando 3 segundos...
timeout /t 3 /nobreak >nul

echo [OK] Aguardado
echo.

echo [3/3] Iniciando sistema...
echo.

REM Iniciar FastAPI
start "FastAPI Backend" cmd /k "cd /d I:\Robo && echo ============================================================ && echo   FASTAPI RODANDO - PORTA 8001 && echo ============================================================ && echo. && venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"

REM Aguardar FastAPI iniciar
timeout /t 5 /nobreak >nul

REM Iniciar React
start "React Dashboard" cmd /k "cd /d I:\Robo\auronex-dashboard && echo ============================================================ && echo   REACT DASHBOARD - PORTA 8501 && echo ============================================================ && echo. && npm run dev"

REM Aguardar React iniciar
timeout /t 3 /nobreak >nul

echo.
echo ======================================================================
echo   SISTEMA INICIADO!
echo ======================================================================
echo.
echo FastAPI: http://localhost:8001
echo Dashboard: http://localhost:8501
echo.
echo Aguarde 10 segundos para tudo inicializar...
echo.
timeout /t 10 /nobreak >nul

REM Abrir dashboard
start http://localhost:8501

echo.
echo ======================================================================
echo   PRONTO! Dashboard deve abrir automaticamente
echo ======================================================================
echo.
pause




