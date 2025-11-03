@echo off
REM ========================================
REM ROBOTRADER - 2 PORTAS APENAS
REM 8001: Django | 8502: Dashboard Dash
REM ========================================

echo ========================================
echo   ROBOTRADER - Sistema Completo
echo ========================================
echo.
echo Iniciando...
echo.

cd /d I:\Robo

REM Matar processos
echo [1/3] Parando processos antigos...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando Django (porta 8001)...
start "RoboTrader - Django" cmd /k "cd /d I:\Robo\saas && ..\venv\Scripts\activate && echo === DJANGO (Porta 8001) === && python manage.py runserver 8001"

timeout /t 10 /nobreak >nul

echo [3/3] Iniciando Dashboard Dash (porta 8502)...
start "RoboTrader - Dashboard" cmd /k "cd /d I:\Robo && venv\Scripts\activate && echo === DASHBOARD DASH (Porta 8502) === && python dashboard_dash_realtime.py"

echo.
echo ========================================
echo   PRONTO!
echo ========================================
echo.
echo PORTAS:
echo - 8001: Django (Admin)
echo - 8502: Dashboard Dash (Usuario)
echo.
echo JANELAS:
echo - 2 janelas abertas (NÃO FECHAR!)
echo - PODE MINIMIZAR ambas
echo - Esta janela PODE FECHAR
echo.
echo Aguarde 15 segundos e acesse:
echo http://localhost:8502
echo.
pause


