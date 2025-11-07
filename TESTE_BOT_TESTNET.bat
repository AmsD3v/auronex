@echo off
REM ====================================
REM TESTAR BOT EM TESTNET BINANCE
REM Inicia bot e monitora trades
REM ====================================

cd /d I:\Robo

echo.
echo ============================================================
echo   TESTE DE BOT - TESTNET BINANCE
echo ============================================================
echo.

REM Pedir ID do bot
set /p BOT_ID="ID do bot (ver no Dashboard): "

echo.
echo Iniciando bot %BOT_ID% em Testnet...
echo.
echo Modo: Bot normal (le config do banco)
echo Pressione Ctrl+C para parar
echo.

REM Ativar venv
call venv\Scripts\activate

REM Iniciar bot
python -m bot.main %BOT_ID%

pause

