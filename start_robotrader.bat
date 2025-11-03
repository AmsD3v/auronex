@echo off
REM Script para iniciar RoboTrader automaticamente
REM Coloque no Startup do Windows para iniciar ao ligar o PC

echo ====================================
echo   ROBOTRADER - Iniciando Sistema
echo ====================================
echo.

cd /d I:\Robo

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Iniciar Django em nova janela
echo [1/2] Iniciando Django (Backend)...
start "RoboTrader - Django" cmd /k "cd I:\Robo\saas && python manage.py runserver 8001"

REM Aguardar 5 segundos
timeout /t 5 /nobreak > nul

REM Iniciar Streamlit em nova janela
echo [2/2] Iniciando Streamlit (Dashboard)...
start "RoboTrader - Streamlit" cmd /k "cd I:\Robo && streamlit run dashboard_master.py --server.port 8501"

echo.
echo ====================================
echo   SISTEMA INICIADO COM SUCESSO!
echo ====================================
echo.
echo Django:    http://localhost:8001
echo Streamlit: http://localhost:8501
echo.
echo Mantenha estas janelas abertas!
echo.
pause


