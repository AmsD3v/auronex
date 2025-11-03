@echo off
REM ========================================
REM DASHBOARD TEMPO REAL - SEM OPACITY!
REM ========================================

echo ========================================
echo   DASHBOARD TEMPO REAL
echo ========================================
echo.
echo Iniciando dashboard SEM opacity...
echo Relógio em tempo real!
echo Auto-save configurações!
echo.

cd /d I:\Robo

REM Matar Streamlit antigo
taskkill /F /IM streamlit.exe >nul 2>&1
timeout /t 2 /nobreak >nul

REM Ativar venv
call venv\Scripts\activate.bat

REM Iniciar dashboard REALTIME
start "RoboTrader - Dashboard RealTime" cmd /k "cd /d I:\Robo && venv\Scripts\activate && streamlit run dashboard_realtime_master.py --server.port 8501"

echo.
echo ========================================
echo   DASHBOARD INICIADO!
echo ========================================
echo.
echo URL: http://localhost:8501
echo.
echo DIFERENÇAS:
echo - ZERO opacity ^(sem piscar^)
echo - Relógio tempo real ^(nunca para^)
echo - Auto-save configurações
echo - Experiência fluida
echo.
echo Feche este CMD mas mantenha a janela do dashboard!
echo.
pause


