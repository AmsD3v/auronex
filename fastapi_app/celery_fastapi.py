"""
Celery Configuration - MESMA lógica do Django
MAS usando SQLAlchemy models do FastAPI

APENAS imports mudam! Lógica do bot é IDÊNTICA!
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('FASTAPI_MODE', 'True')

app = Celery('robotrader_fastapi')
app.config_from_object('redis://localhost:6379/0')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/1'
app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def run_trading_bot(bot_config_id):
    """
    Tarefa principal - MESMA lógica do Django!
    Apenas imports mudam!
    """
    # Imports do FastAPI
    from .models import BotConfiguration, Trade, ExchangeAPIKey
    from .database import SessionLocal
    from decimal import Decimal
    import ccxt
    from datetime import datetime
    
    db = SessionLocal()
    
    try:
        bot_config = db.query(BotConfiguration).filter(BotConfiguration.id == bot_config_id).first()
        
        if not bot_config or not bot_config.is_active:
            return "Bot não está ativo"
        
        # Buscar API keys
        api_key_obj = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == bot_config.user_id,
            ExchangeAPIKey.exchange == bot_config.exchange,
            ExchangeAPIKey.is_active == True
        ).first()
        
        if not api_key_obj:
            return "API Key não encontrada"
        
        # Descriptografar keys
        from .utils.encryption import decrypt_data
        api_key_decrypted = decrypt_data(api_key_obj.api_key_encrypted)
        secret_decrypted = decrypt_data(api_key_obj.secret_key_encrypted)
        
        # Conectar exchange
        exchange_class = getattr(ccxt, bot_config.exchange)
        exchange = exchange_class({
            'apiKey': api_key_decrypted,
            'secret': secret_decrypted,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,
                'recvWindow': 60000
            }
        })
        
        if api_key_obj.is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Sincronizar timestamp
        try:
            exchange.load_time_difference()
        except:
            pass
        
        # RESTANTE DA LÓGICA É IGUAL AO DJANGO!
        # (Vou copiar do celery_config.py depois)
        
        trades_executados = 0
        MAX_POSITIONS = 3
        
        for symbol in bot_config.symbols:
            try:
                # Buscar trades abertos
                open_trades = db.query(Trade).filter(
                    Trade.user_id == bot_config.user_id,
                    Trade.bot_config_id == bot_config.id,
                    Trade.symbol == symbol,
                    Trade.status == 'open'
                ).all()
                
                # Buscar preço atual
                ticker = exchange.fetch_ticker(symbol)
                current_price = Decimal(str(ticker['last']))
                
                # Se tem posição aberta, verificar saída
                if open_trades:
                    for open_trade in open_trades:
                        should_exit = False
                        exit_reason = ""
                        
                        # Calcular P&L
                        pnl_percent = ((current_price - open_trade.entry_price) / open_trade.entry_price) * 100
                        
                        # Take Profit
                        if pnl_percent >= float(bot_config.take_profit_percent):
                            should_exit = True
                            exit_reason = f"Take Profit ({pnl_percent:.1f}%)"
                        
                        # Stop Loss
                        elif pnl_percent <= -float(bot_config.stop_loss_percent):
                            should_exit = True
                            exit_reason = f"Stop Loss ({pnl_percent:.1f}%)"
                        
                        # Trailing Stop
                        elif open_trade.highest_price:
                            if current_price > open_trade.highest_price:
                                open_trade.highest_price = current_price
                            
                            trailing_stop_price = open_trade.highest_price * Decimal('0.97')
                            if current_price <= trailing_stop_price:
                                should_exit = True
                                pnl_from_high = ((current_price - open_trade.highest_price) / open_trade.highest_price) * 100
                                exit_reason = f"Trailing Stop (caiu {abs(pnl_from_high):.1f}% do pico)"
                        
                        if should_exit:
                            # VENDER
                            try:
                                order = exchange.create_market_order(symbol, 'sell', float(open_trade.quantity))
                                
                                # Atualizar trade
                                open_trade.exit_price = current_price
                                open_trade.exit_time = datetime.now()
                                open_trade.profit_loss = (current_price - open_trade.entry_price) * open_trade.quantity
                                open_trade.profit_loss_percent = pnl_percent
                                open_trade.status = 'closed'
                                
                                db.commit()
                                
                                print(f"🔴 VENDA: {symbol} @ ${current_price:.2f} | {exit_reason} | P&L: {pnl_percent:+.2f}%")
                                trades_executados += 1
                                
                            except Exception as e:
                                print(f"Erro ao fechar trade {symbol}: {e}")
                        else:
                            # Atualizar highest_price se necessário
                            if open_trade.highest_price is None or current_price > open_trade.highest_price:
                                open_trade.highest_price = current_price
                                db.commit()
                
                # Se não tem posição ou pode adicionar (pyramiding)
                else:
                    num_positions = db.query(Trade).filter(
                        Trade.user_id == bot_config.user_id,
                        Trade.bot_config_id == bot_config.id,
                        Trade.symbol == symbol,
                        Trade.status == 'open'
                    ).count()
                    
                    if num_positions < MAX_POSITIONS:
                        # Buscar histórico para calcular média
                        ohlcv = exchange.fetch_ohlcv(symbol, bot_config.timeframe, limit=50)
                        
                        if len(ohlcv) < 50:
                            continue
                        
                        prices = [candle[4] for candle in ohlcv]
                        avg_price = sum(prices) / len(prices)
                        
                        # FILTRO ULTRA AGRESSIVO: 0.1% abaixo
                        if current_price < Decimal(str(avg_price)) * Decimal('0.999'):
                            # COMPRAR
                            try:
                                capital_per_trade = bot_config.capital / len(bot_config.symbols)
                                capital_per_position = capital_per_trade / MAX_POSITIONS
                                quantity = capital_per_position / current_price
                                
                                # Validar quantidade mínima
                                market = exchange.market(symbol)
                                min_qty = market['limits']['amount']['min'] or 0.001
                                if quantity < Decimal(str(min_qty)):
                                    quantity = Decimal(str(min_qty))
                                
                                # Executar ordem
                                order = exchange.create_market_order(symbol, 'buy', float(quantity))
                                
                                # Criar trade no banco
                                trade = Trade(
                                    user_id=bot_config.user_id,
                                    bot_config_id=bot_config.id,
                                    exchange=bot_config.exchange,
                                    symbol=symbol,
                                    side='buy',
                                    entry_price=current_price,
                                    quantity=quantity,
                                    entry_time=datetime.now(),
                                    status='open',
                                    highest_price=current_price
                                )
                                
                                db.add(trade)
                                db.commit()
                                
                                print(f"🟢 COMPRA ({num_positions+1}/{MAX_POSITIONS}): {symbol} @ ${current_price:.2f} | Qtd: {quantity:.6f}")
                                trades_executados += 1
                                
                            except Exception as e:
                                print(f"Erro ao abrir trade {symbol}: {e}")
                
            except Exception as e:
                print(f"Erro ao processar {symbol}: {e}")
        
        return f"Bot executado: {trades_executados} trades realizados em {len(bot_config.symbols)} símbolos"
        
    finally:
        db.close()


@app.task
def check_active_bots():
    """Verifica quais bots estão ativos e executa"""
    from .models import BotConfiguration
    from .database import SessionLocal
    
    db = SessionLocal()
    
    try:
        active_bots = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all()
        
        for bot in active_bots:
            run_trading_bot.delay(bot.id)
        
        return f"{len(active_bots)} bots ativos"
    finally:
        db.close()


# Tarefas periódicas
app.conf.beat_schedule = {
    'run-active-bots-every-second': {
        'task': 'fastapi_app.celery_fastapi.check_active_bots',
        'schedule': 1.0,  # A cada 1 segundo!
    },
}


