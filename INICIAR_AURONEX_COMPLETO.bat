@echo off
chcp 65001 >nul
title AURONEX ROBO TRADER - Sistema Completo
color 0A

echo ========================================
echo   AURONEX ROBO TRADER - INICIANDO
echo ========================================
echo.

cd /d "%~dp0"

echo [1/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERRO: venv nao encontrado!
    pause
    exit /b 1
)
echo OK - Ambiente ativado
echo.

echo [2/5] Iniciando FastAPI (Backend)...
start /b uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload
echo OK - FastAPI rodando na porta 8001
timeout /t 3 /nobreak >nul
echo.

echo [3/5] Iniciando Streamlit (Dashboard Visual)...
start /b streamlit run dashboard_streamlit_fastapi.py --server.port 8501 --server.headless true
echo OK - Streamlit rodando na porta 8501
timeout /t 3 /nobreak >nul
echo.

echo [4/5] Celery (DESABILITADO - Requer Redis)
echo INFO - Bot funciona via API (nao precisa Celery agora)
echo.

echo ========================================
echo   SISTEMA AURONEX ONLINE!
echo ========================================
echo.
echo URLs:
echo   FastAPI:    http://localhost:8001/
echo   Streamlit:  http://localhost:8501/
echo   Admin:      http://localhost:8001/admin/
echo.
echo Login Admin:
echo   Email: admin@robotrader.com
echo   Senha: admin123
echo.
echo ========================================
echo   SISTEMA RODANDO EM BACKGROUND
echo ========================================
echo.
echo Todos os servicos estao rodando!
echo.
echo Para PARAR o sistema:
echo   - Feche esta janela OU
echo   - Execute: PARAR_AURONEX.bat
echo.
echo Pressione qualquer tecla para verificar status...
pause >nul

:LOOP
cls
echo ========================================
echo   AURONEX - STATUS DOS SERVICOS
echo ========================================
echo.

echo Verificando FastAPI (porta 8001)...
netstat -ano | findstr ":8001" >nul
if errorlevel 1 (
    echo   [X] FastAPI: PARADO
) else (
    echo   [OK] FastAPI: RODANDO
)

echo Verificando Streamlit (porta 8501)...
netstat -ano | findstr ":8501" >nul
if errorlevel 1 (
    echo   [X] Streamlit: PARADO
) else (
    echo   [OK] Streamlit: RODANDO
)

echo.
echo ========================================
echo.
echo Pressione CTRL+C para parar tudo
echo Ou feche esta janela
echo.
timeout /t 10 /nobreak >nul
goto LOOP

