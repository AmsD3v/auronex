@echo off
chcp 65001 >nul
title Auronex - Iniciar Dashboards
color 0A

echo ========================================
echo   AURONEX - INICIAR DASHBOARDS
echo ========================================
echo.
echo Iniciando 2 serviços:
echo   1. FastAPI + Bot Controller (porta 8001)
echo   2. Streamlit Dashboard (porta 8501)
echo.
echo ⏰ Aguarde 30-40 segundos para inicialização completa...
echo.
echo ========================================
echo.

REM Ir para pasta do projeto
cd /d I:\Robo

REM ========================================
REM 1. FASTAPI + BOT CONTROLLER
REM ========================================

echo 1️⃣  Iniciando FastAPI + Bot Controller...
echo.

REM Abrir FastAPI + Bot em CMD SEPARADO
start "FastAPI + Bot Controller" cmd /k "cd /d I:\Robo && echo ======================================== && echo   FASTAPI + BOT CONTROLLER && echo ======================================== && echo. && .\venv\Scripts\python.exe -m uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 --reload"

REM Aguardar FastAPI iniciar
timeout /t 10 /nobreak >nul

REM ========================================
REM 2. STREAMLIT DASHBOARD
REM ========================================

echo 2️⃣  Iniciando Streamlit Dashboard...
echo.

REM Abrir Streamlit em CMD SEPARADO
start "Streamlit Dashboard" cmd /k "cd /d I:\Robo && echo ======================================== && echo   STREAMLIT DASHBOARD && echo ======================================== && echo. && .\venv\Scripts\streamlit.exe run dashboard_streamlit_fastapi.py --server.port 8501"

REM Aguardar Streamlit iniciar
timeout /t 15 /nobreak >nul

REM ========================================
REM VERIFICAÇÃO E ABERTURA AUTOMÁTICA
REM ========================================

echo.
echo ========================================
echo   ✅ SERVIÇOS INICIADOS!
echo ========================================
echo.
echo 2 janelas PowerShell foram abertas:
echo   - FastAPI + Bot Controller (azul)
echo   - Streamlit Dashboard (verde)
echo.
echo ⚠️  NÃO FECHE AS JANELAS!
echo.
echo ========================================
echo   ACESSAR SISTEMA
echo ========================================
echo.
echo 🌐 URLs Locais:
echo.
echo   Site Principal:
echo     http://localhost:8001/
echo.
echo   Dashboard Streamlit:
echo     http://localhost:8501/
echo.
echo   Documentação API:
echo     http://localhost:8001/api/docs
echo.
echo ========================================
echo   STATUS DOS SERVIÇOS
echo ========================================
echo.

REM Aguardar um pouco mais
timeout /t 5 /nobreak >nul

echo Verificando portas...
echo.

REM Verificar FastAPI
netstat -ano | findstr :8001 >nul
if %ERRORLEVEL% EQU 0 (
    echo   ✅ FastAPI: RODANDO ^(porta 8001^)
) else (
    echo   ❌ FastAPI: NÃO INICIOU
)

REM Verificar Streamlit
netstat -ano | findstr :8501 >nul
if %ERRORLEVEL% EQU 0 (
    echo   ✅ Streamlit: RODANDO ^(porta 8501^)
) else (
    echo   ❌ Streamlit: NÃO INICIOU
)

echo.
echo ========================================
echo   🚀 ABRIR NAVEGADOR?
echo ========================================
echo.

set /p ABRIR="Abrir navegador automaticamente? (S/N): "

if /i "%ABRIR%"=="S" (
    echo.
    echo Abrindo navegadores...
    
    REM Aguardar mais um pouco
    timeout /t 5 /nobreak >nul
    
    REM Abrir site
    start http://localhost:8001/
    
    REM Aguardar 2 segundos
    timeout /t 2 /nobreak >nul
    
    REM Abrir dashboard
    start http://localhost:8501/
    
    echo.
    echo ✅ Navegadores abertos!
)

echo.
echo ========================================
echo   SISTEMA OPERACIONAL
echo ========================================
echo.
echo ⚠️  Para PARAR os serviços:
echo     Feche as janelas PowerShell abertas
echo     OU pressione Ctrl+C em cada uma
echo.
echo 🔄 Para REINICIAR:
echo     Execute este arquivo novamente
echo.
echo ========================================
echo   Auronex v1.0-A1
echo   Sistema pronto!
echo ========================================
echo.

pause

