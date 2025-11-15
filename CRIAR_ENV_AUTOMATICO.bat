@echo off
chcp 65001 >nul
REM ========================================
REM CRIAR .ENV AUTOMATICAMENTE
REM ========================================

echo ======================================================================
echo   SETUP AUTOMATICO - AURONEX .ENV
echo ======================================================================
echo.

REM Verificar se .env já existe
if exist .env (
    echo [AVISO] Arquivo .env ja existe!
    echo.
    echo Fazendo backup...
    copy .env .env.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2% >nul 2>&1
    echo [OK] Backup criado
    echo.
)

REM Criar .env
echo [1/2] Criando arquivo .env...

(
echo # ========================================
echo # AURONEX TRADING BOT - Configuracao LOCAL
echo # ========================================
echo # Gerado automaticamente em: 14/11/2025
echo.
echo # ========================================
echo # SEGURANCA - CRITICO
echo # ========================================
echo.
echo # Chave de criptografia para API Keys
echo ENCRYPTION_KEY=3zHzFSUpbptbx2sOSG1E9eAVpT0egw9aWFsczVtcq44=
echo.
echo # Chave secreta para JWT tokens
echo SECRET_KEY=9f05ab3f6c9eea75e00ada9ebac1a8293107273420c167a332c385e11e6b9105
echo.
echo # Algoritmo JWT
echo ALGORITHM=HS256
echo.
echo # Expiracao dos tokens
echo ACCESS_TOKEN_EXPIRE_MINUTES=15
echo REFRESH_TOKEN_EXPIRE_DAYS=7
echo.
echo # ========================================
echo # CORS - Origens Permitidas
echo # ========================================
echo.
echo ALLOWED_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
echo.
echo # ========================================
echo # AMBIENTE
echo # ========================================
echo.
echo ENVIRONMENT=development
echo DEBUG_MODE=True
echo LOG_LEVEL=INFO
echo.
echo # ========================================
echo # BANCO DE DADOS
echo # ========================================
echo.
echo DATABASE_URL=sqlite:///./db.sqlite3
echo.
echo # ========================================
echo # BOT TRADING
echo # ========================================
echo.
echo PAPER_TRADING=True
echo USE_TESTNET=True
echo TRADING_SYMBOL=BTC/USDT
echo TIMEFRAME=15m
echo STRATEGY=trend_following
echo POSITION_SIZE_PERCENT=0.10
echo STOP_LOSS_PERCENT=0.02
echo TAKE_PROFIT_PERCENT=0.04
echo MAX_DRAWDOWN_PERCENT=0.10
echo MAX_TRADES_PER_DAY=10
echo.
echo # ========================================
echo # EXCHANGES
echo # ========================================
echo.
echo BINANCE_TESTNET_API_KEY=
echo BINANCE_TESTNET_SECRET_KEY=
echo.
echo # ========================================
echo # NOTIFICACOES
echo # ========================================
echo.
echo TELEGRAM_BOT_TOKEN=
echo TELEGRAM_CHAT_ID=
echo ENABLE_TELEGRAM=False
echo SLACK_WEBHOOK_URL=
echo DISCORD_WEBHOOK_URL=
echo.
echo # ========================================
echo # CACHE
echo # ========================================
echo.
echo REDIS_URL=redis://localhost:6379/0
echo.
echo # ========================================
echo # SISTEMA
echo # ========================================
echo.
echo UPDATE_INTERVAL=60
echo SAVE_HISTORICAL_DATA=True
) > .env

echo [OK] Arquivo .env criado!
echo.

REM Verificar
echo [2/2] Verificando arquivo...
if exist .env (
    for %%A in (.env) do echo [OK] Tamanho: %%~zA bytes
    echo.
) else (
    echo [ERRO] Arquivo .env nao foi criado!
    pause
    exit /b 1
)

echo ======================================================================
echo   CONFIGURACAO CONCLUIDA!
echo ======================================================================
echo.
echo Chaves configuradas:
echo   - ENCRYPTION_KEY (44 chars)
echo   - SECRET_KEY (64 chars)
echo   - CORS: localhost:8501
echo   - Ambiente: development
echo.
echo ======================================================================
echo   PROXIMOS PASSOS:
echo ======================================================================
echo.
echo 1. Se tem API Keys antigas:
echo    python scripts/migrate_encryption.py
echo.
echo 2. Reinicie os servicos:
echo    MATAR_TUDO.bat
echo    TESTAR_SERVER_LOCAL_09_11_25.bat
echo.
echo 3. Teste:
echo    http://localhost:8501
echo.
echo ======================================================================
echo [ATENCAO] NUNCA commite o .env no Git!
echo ======================================================================
echo.
pause






