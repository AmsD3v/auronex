@echo off
chcp 65001 >nul
title Auronex - Iniciar 3 Sistemas
color 0E

echo ========================================
echo   AURONEX - 3 SISTEMAS SEPARADOS
echo ========================================
echo.
echo Abrindo 3 CMDs:
echo   1. FastAPI (porta 8001)
echo   2. Bot Controller (integrado no FastAPI)
echo   3. Streamlit Dashboard (porta 8501)
echo.
echo ⚠️  Aguarde 30 segundos para tudo iniciar!
echo.
echo ========================================
echo.

cd /d I:\Robo

REM ========================================
REM CMD 1: FASTAPI + BOT CONTROLLER
REM ========================================

echo 1️⃣  FastAPI + Bot Controller...

start "1. FastAPI + Bot" cmd /k "title 1. FastAPI + Bot && cd /d I:\Robo && color 0A && echo ======================================== && echo   FASTAPI + BOT CONTROLLER && echo ======================================== && echo. && echo Porta: 8001 && echo Bot Controller: ATIVO && echo. && .\venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"

timeout /t 12 /nobreak >nul

REM ========================================
REM CMD 2: STREAMLIT DASHBOARD
REM ========================================

echo 2️⃣  Streamlit Dashboard...

start "2. Streamlit Dashboard" cmd /k "title 2. Streamlit Dashboard && cd /d I:\Robo && color 0B && echo ======================================== && echo   STREAMLIT DASHBOARD && echo ======================================== && echo. && echo Porta: 8501 && echo. && .\venv\Scripts\streamlit.exe run dashboard_streamlit_fastapi.py --server.port 8501"

timeout /t 15 /nobreak >nul

REM ========================================
REM VERIFICAÇÃO
REM ========================================

echo.
echo ========================================
echo   ✅ SISTEMAS INICIADOS!
echo ========================================
echo.
echo 2 janelas CMD abertas:
echo   - CMD 1: FastAPI + Bot (verde)
echo   - CMD 2: Streamlit (azul)
echo.
echo ⚠️  NÃO FECHE AS JANELAS CMD!
echo.
echo ========================================
echo   ACESSAR SISTEMA
echo ========================================
echo.
echo 🌐 Site Principal:
echo     http://localhost:8001/
echo.
echo 📊 Dashboard Streamlit:
echo     http://localhost:8501/
echo.
echo 📚 API Docs:
echo     http://localhost:8001/api/docs
echo.
echo ========================================
echo   ABRIR NAVEGADOR?
echo ========================================
echo.

set /p ABRIR="Abrir navegadores? (S/N): "

if /i "%ABRIR%"=="S" (
    echo.
    echo Abrindo navegadores...
    timeout /t 3 /nobreak >nul
    start http://localhost:8001/
    timeout /t 2 /nobreak >nul
    start http://localhost:8501/
    echo ✅ Navegadores abertos!
)

echo.
echo ========================================
echo   Sistema Auronex v1.0-A2
echo   23+ horas de desenvolvimento
echo ========================================
echo.
echo Para PARAR:
echo   Feche as janelas CMD abertas
echo   OU pressione Ctrl+C em cada uma
echo.

pause

