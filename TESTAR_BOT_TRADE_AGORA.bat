@echo off
title TESTE BOT - TRADE REAL TESTNET
REM ====================================
REM TESTE DE BOT COM CONFIG DO DASHBOARD
REM Testa se bot le: velocidade, cryptos, exchange
REM ====================================

cd /d I:\Robo
call venv\Scripts\activate

cls
echo.
echo ============================================================
echo   TESTE BOT - LENDO CONFIG DO DASHBOARD REACT
echo ============================================================
echo.

REM Ver bots disponiveis
echo Consultando bots no banco...
python -c "from fastapi_app.database import SessionLocal; from fastapi_app.models import BotConfiguration; db = SessionLocal(); bots = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all(); print('Bots ativos:'); [print(f'  ID {b.id}: {b.name} - {b.exchange.upper()} - {b.symbols}') for b in bots]; db.close()"

echo.
set /p BOT_ID="Digite o ID do bot para testar: "

echo.
echo ============================================================
echo   INICIANDO BOT %BOT_ID%
echo   Configuracoes virao do Dashboard React!
echo ============================================================
echo.
echo O bot vai:
echo   - Ler exchange, cryptos, velocidade do banco
echo   - Conectar na exchange em TESTNET
echo   - Analisar mercado
echo   - Fazer trades (testnet - dinheiro falso!)
echo.
echo Pressione Ctrl+C para parar
echo.
echo ============================================================
echo.

python -m bot.main %BOT_ID%

pause


