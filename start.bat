@echo off
REM ========================================
REM RoboTrader - Script de Inicialização
REM ========================================

cd /d "%~dp0"

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Limpar tela
cls

REM Banner
echo.
echo ========================================
echo    ROBOTRADER - Bot de Trading
echo ========================================
echo.
echo Ambiente virtual ativado!
echo.
echo Comandos disponiveis:
echo   [1] Testar conexao    : python scripts/test_connection.py
echo   [2] Baixar dados      : python scripts/download_data.py --days 7
echo   [3] Executar backtest : python scripts/run_backtest.py
echo   [4] Executar bot      : python main.py
echo.
echo Para sair: digite 'exit' ou feche a janela
echo ========================================
echo.

REM Manter terminal aberto
cmd /k

