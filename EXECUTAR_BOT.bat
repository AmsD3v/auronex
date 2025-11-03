@echo off
echo ========================================
echo   AURONEX TRADING BOT
echo ========================================
echo.
echo Escolha o modo:
echo   1 - BACKTEST (Teste seguro com dados historicos)
echo   2 - TRADING REAL (Opera com dinheiro real!)
echo.
set /p modo="Digite 1 ou 2: "

if "%modo%"=="1" (
    echo.
    echo ========================================
    echo   MODO BACKTEST
    echo ========================================
    echo.
    set /p bot_id="ID do Bot (veja em http://localhost:8001/bots-page): "
    
    cd /d I:\Robo
    call venv\Scripts\activate.bat
    
    echo.
    echo Executando backtest do bot !bot_id!...
    echo.
    python bot/main.py !bot_id! --backtest --start-date 2024-01-01 --end-date 2024-12-31 --capital 1000
    
    echo.
    echo ========================================
    echo   BACKTEST CONCLUIDO!
    echo ========================================
    pause
    
) else if "%modo%"=="2" (
    echo.
    echo ========================================
    echo   MODO TRADING REAL
    echo ========================================
    echo.
    echo ATENCAO: Bot fara trades REAIS!
    echo Certifique-se de:
    echo   - API Key configurada corretamente
    echo   - Saldo suficiente na corretora
    echo   - Estrategia testada em backtest
    echo.
    set /p confirma="Confirma execucao REAL? (S/N): "
    
    if /i "!confirma!"=="S" (
        set /p bot_id="ID do Bot: "
        
        cd /d I:\Robo
        call venv\Scripts\activate.bat
        
        echo.
        echo Executando bot !bot_id! em PRODUCAO...
        echo Pressione CTRL+C para parar
        echo.
        python bot/main.py !bot_id!
    ) else (
        echo.
        echo Operacao cancelada.
        pause
    )
) else (
    echo.
    echo Opcao invalida!
    pause
)



