@echo off
echo ===================================
echo   AURONEX - BACKEND FASTAPI
echo ===================================
echo.

REM Verificar se venv existe
if not exist "venv\Scripts\activate.bat" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo.
    echo Crie o venv primeiro:
    echo python -m venv venv
    echo.
    pause
    exit /b 1
)

echo [OK] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [OK] Verificando uvicorn...
python -c "import uvicorn" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Uvicorn nao instalado!
    echo [INFO] Instalando dependencias...
    echo.
    pip install -r requirements.txt
    echo.
)

echo ===================================
echo   INICIANDO BACKEND FASTAPI
echo ===================================
echo.
echo URL: http://localhost:8001
echo Docs: http://localhost:8001/api/docs
echo Health: http://localhost:8001/health
echo.
echo Aguarde o servidor iniciar...
echo (Pressione Ctrl+C para parar)
echo.

REM Iniciar FastAPI
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload

pause

