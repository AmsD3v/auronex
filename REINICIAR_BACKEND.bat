@echo off
REM ========================================
REM REINICIAR BACKEND FASTAPI
REM Aplica novos limites dos planos
REM ========================================

echo.
echo ============================================================
echo   REINICIANDO BACKEND FASTAPI
echo   (Aplicando novos limites de planos)
echo ============================================================
echo.

REM Ir para pasta raiz
cd /d "%~dp0"

REM Ativar venv
echo [1/2] Ativando ambiente virtual Python...
call venv\Scripts\activate

echo [2/2] Iniciando FastAPI...
echo.
echo ============================================================
echo   BACKEND INICIANDO...
echo   URL: http://localhost:8001
echo   Docs: http://localhost:8001/api/docs
echo ============================================================
echo.

uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload

pause
