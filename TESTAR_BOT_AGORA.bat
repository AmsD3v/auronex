@echo off
REM ====================================
REM TESTAR BOT FAZENDO TRADES
REM Modo direto - Ver trades acontecendo
REM ====================================

cd /d I:\Robo
call venv\Scripts\activate

cls
echo.
echo ============================================================
echo   TESTAR BOT - VER TRADES ACONTECENDO
echo ============================================================
echo.

REM Ver bot ativo
python -c "from fastapi_app.database import SessionLocal; from fastapi_app.models import BotConfiguration; db = SessionLocal(); bot = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).first(); print(f'Bot ATIVO: {bot.id if bot else \"Nenhum\"}'); db.close()"

echo.
set /p BOT_ID="Digite ID do bot para testar (38): "
if "%BOT_ID%"=="" set BOT_ID=38

echo.
echo ============================================================
echo   INICIANDO BOT %BOT_ID% - MODO TRADE REAL
echo ============================================================
echo.
echo Voce vai ver:
echo   - Analises a cada 1-5s
echo   - Sinais de compra/venda
echo   - TRADES EXECUTADOS (testnet)
echo   - Trades SALVOS no banco
echo.
echo Pressione Ctrl+C para parar
echo.
echo ============================================================
echo.

REM Executar bot DIRETO (sem controller)
python -m bot.main_enterprise_async %BOT_ID%

pause

