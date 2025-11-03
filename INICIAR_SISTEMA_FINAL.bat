@echo off
REM ========================================
REM ROBOTRADER - SISTEMA FINAL SIMPLIFICADO
REM APENAS 2 PORTAS!
REM ========================================

echo ========================================
echo   ROBOTRADER - Sistema Final
echo ========================================
echo.
echo Iniciando sistema completo...
echo.
echo PORTAS:
echo - 8001: Django ^(Backend + Admin^)
echo - 8502: Dashboard Dash ^(Usuario^)
echo.

cd /d I:\Robo

REM Matar processos antigos
echo [1/3] Limpando processos...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM streamlit.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo [2/3] Iniciando Django (porta 8001)...
start "RoboTrader - Django Backend" cmd /k "cd /d I:\Robo\saas && ..\venv\Scripts\activate && python manage.py runserver 8001"

echo [3/3] Aguardando Django (10s) e iniciando Dashboard Dash...
timeout /t 10 /nobreak >nul

start "RoboTrader - Dashboard Dash" cmd /k "cd /d I:\Robo && venv\Scripts\activate && python dashboard_dash_realtime.py"

echo.
echo ========================================
echo   SISTEMA INICIADO!
echo ========================================
echo.
echo ACESSE:
echo.
echo Admin Panel:     http://localhost:8001/admin/
echo Dashboard Usuario: http://localhost:8502
echo.
echo IMPORTANTE:
echo - Mantenha as 2 janelas abertas ^(Django e Dash^)
echo - PODE FECHAR ESTA janela ^(este CMD^)
echo - Para parar: Feche as janelas Django e Dash
echo.
echo Aguarde 15 segundos e acesse Dashboard:
echo http://localhost:8502
echo.
pause


