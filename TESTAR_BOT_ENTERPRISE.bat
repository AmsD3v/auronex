@echo off
REM ========================================
REM TESTAR BOT ENTERPRISE EM TESTNET
REM Ultra rápido + Modo Caçador
REM ========================================

echo.
echo ============================================================
echo   TESTE DO BOT ENTERPRISE - TESTNET BINANCE
echo   Ultra Rapido + Modo Cacador de Oportunidades
echo ============================================================
echo.

cd /d I:\Robo

REM Ativar venv
call venv\Scripts\activate

echo.
echo Opcoes de teste:
echo.
echo 1. Bot Ultra Rapido (5s entre analises)
echo 2. Bot Cacador (1s + micro oscilacoes)
echo 3. Bot Scalper (1s + scalping)
echo.

set /p MODO="Escolha (1-3): "

REM Configurar baseado na escolha
if "%MODO%"=="1" (
    set SPEED=5
    set HUNTER=
    set DESCRICAO=Ultra Rapido (5s)
)

if "%MODO%"=="2" (
    set SPEED=3
    set HUNTER=--hunter
    set DESCRICAO=Cacador (3s + micro oscilacoes)
)

if "%MODO%"=="3" (
    set SPEED=1
    set HUNTER=--hunter
    set DESCRICAO=Scalper (1s + ultra rapido)
)

echo.
echo ============================================================
echo   INICIANDO: %DESCRICAO%
echo ============================================================
echo.

REM Pedir ID do bot
set /p BOT_ID="ID do bot (ver em Dashboard React): "

echo.
echo Iniciando bot %BOT_ID%...
echo Velocidade: %SPEED%s
echo Modo Cacador: %HUNTER%
echo.
echo Pressione Ctrl+C para parar
echo.

REM Executar bot enterprise
python bot/main_enterprise.py %BOT_ID% --speed %SPEED% %HUNTER%

pause

