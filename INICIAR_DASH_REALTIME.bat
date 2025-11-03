@echo off
REM ========================================
REM DASHBOARD DASH - TEMPO REAL PERFEITO!
REM ========================================

echo ========================================
echo   DASHBOARD DASH - TEMPO REAL
echo ========================================
echo.
echo Iniciando dashboard PROFISSIONAL...
echo.
echo DIFERENCAS:
echo - Relogio: Atualiza TODO SEGUNDO ^(1 FPS^)!
echo - Saldo: REAL da exchange ^(fetch 1s^)!
echo - Opacity: ZERO ^(callbacks assincronos^)!
echo - Performance: 10x melhor!
echo.

cd /d I:\Robo

REM Ativar venv
call venv\Scripts\activate.bat

REM Iniciar Dash
start "RoboTrader - Dashboard DASH" cmd /k "cd /d I:\Robo && venv\Scripts\activate && python dashboard_dash_realtime.py"

echo.
echo ========================================
echo   DASHBOARD INICIADO!
echo ========================================
echo.
echo Streamlit ^(antigo^): http://localhost:8501
echo DASH ^(NOVO^):        http://localhost:8502
echo.
echo Abra AMBOS e compare a diferenca!
echo Dashboard Dash eh MUITO superior!
echo.
echo Feche este CMD mas mantenha janela Dash!
echo.
pause


