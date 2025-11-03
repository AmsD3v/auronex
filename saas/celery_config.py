"""
Celery Configuration - RoboTrader SaaS
Engine para rodar bots em background
"""

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas.settings')

app = Celery('robotrader_saas')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def run_trading_bot(bot_config_id):
    """
    Tarefa principal - roda bot de trading com gestão completa de trades
    """
    from bots.models import BotConfiguration, Trade
    from users.models import ExchangeAPIKey
    from django.contrib.auth.models import User
    from django.utils import timezone
    from decimal import Decimal
    import ccxt
    
    bot_config = BotConfiguration.objects.get(id=bot_config_id)
    
    if not bot_config.is_active:
        return "Bot não está ativo"
    
    # Buscar API keys
    api_key_obj = bot_config.user.api_keys.filter(
        exchange=bot_config.exchange,
        is_active=True
    ).first()
    
    if not api_key_obj:
        return "API Key não encontrada"
    
    # Conectar exchange
    exchange_class = getattr(ccxt, bot_config.exchange)
    exchange = exchange_class({
        'apiKey': api_key_obj.api_key,
        'secret': api_key_obj.secret_key,
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
    
    # Lógica de trading para cada símbolo
    trades_executados = 0
    
    for symbol in bot_config.symbols:
        try:
            # Verificar se já tem posição aberta para este símbolo
            open_trade = Trade.objects.filter(
                user=bot_config.user,
                bot_config=bot_config,
                symbol=symbol,
                status='open'
            ).first()
            
            ticker = exchange.fetch_ticker(symbol)
            current_price = Decimal(str(ticker['last']))
            
            # Verificar TODAS posições abertas (pode ter múltiplas com pyramiding)
            open_trades = Trade.objects.filter(
                user=bot_config.user,
                bot_config=bot_config,
                symbol=symbol,
                status='open'
            )
            
            if open_trades.exists():
                # ✅ TEM POSIÇÃO(ÕES) ABERTA(S) - GERENCIAR SAÍDA
                for open_trade in open_trades:
                    entry_price = open_trade.entry_price
                    price_change_percent = ((current_price - entry_price) / entry_price) * 100
                    
                    # ✅ TRAILING STOP - Atualizar highest_price
                    if open_trade.highest_price is None or current_price > open_trade.highest_price:
                        open_trade.highest_price = current_price
                        open_trade.save()
                    
                    should_exit = False
                    exit_reason = ""
                    
                    # Stop Loss fixo
                    if price_change_percent <= -bot_config.stop_loss_percent:
                        should_exit = True
                        exit_reason = "Stop Loss"
                    
                    # ✅ TRAILING STOP (3% abaixo do pico)
                    elif open_trade.highest_price:
                        trailing_stop_price = open_trade.highest_price * Decimal('0.97')  # 3% abaixo do pico
                        if current_price <= trailing_stop_price:
                            should_exit = True
                            pnl_from_high = ((current_price - open_trade.highest_price) / open_trade.highest_price) * 100
                            exit_reason = f"Trailing Stop (caiu {abs(pnl_from_high):.1f}% do pico)"
                    
                    # Take Profit fixo (backup caso não pegue trailing)
                    elif price_change_percent >= bot_config.take_profit_percent:
                        should_exit = True
                        exit_reason = "Take Profit"
                    
                    if should_exit:
                        # VENDER (fechar posição)
                        try:
                            # Executar ordem de venda na exchange
                            order = exchange.create_market_order(symbol, 'sell', float(open_trade.quantity))
                            
                            # Calcular lucro/prejuízo
                            pnl = (current_price - entry_price) * open_trade.quantity
                            pnl_percent = price_change_percent
                            
                            # ATUALIZAR O TRADE NO BANCO
                            open_trade.exit_price = current_price
                            open_trade.exit_time = timezone.now()
                            open_trade.profit_loss = pnl
                            open_trade.profit_loss_percent = pnl_percent
                            open_trade.status = 'closed'
                            open_trade.save()
                            
                            trades_executados += 1
                            
                            emoji = "💰" if pnl > 0 else "❌"
                            highest_gain = ((open_trade.highest_price - entry_price) / entry_price) * 100 if open_trade.highest_price else 0
                            print(f"{emoji} {exit_reason}: {symbol} | P&L: ${pnl:.2f} ({pnl_percent:+.2f}%) | Pico: +{highest_gain:.1f}%")
                            
                        except Exception as e:
                            print(f"Erro ao fechar trade {symbol}: {e}")
                        
            else:
                # NÃO TEM POSIÇÃO OU PODE ADICIONAR (PYRAMIDING)
                # Contar posições abertas
                num_positions = Trade.objects.filter(
                    user=bot_config.user,
                    bot_config=bot_config,
                    symbol=symbol,
                    status='open'
                ).count()
                
                # ✅ PYRAMIDING: Permitir até 3 posições por símbolo
                MAX_POSITIONS = 3
                
                if num_positions < MAX_POSITIONS:
                    # PROCURAR ENTRADA
                    ohlcv = exchange.fetch_ohlcv(symbol, bot_config.timeframe, limit=20)
                    if len(ohlcv) < 20:
                        continue
                    
                    prices = [candle[4] for candle in ohlcv]  # close prices
                    avg_price = sum(prices) / len(prices)
                    
                    # ✅ ULTRA AGRESSIVO: Filtro -0.1% (para testes rápidos!)
                    # Permite MÁXIMO de entradas! Primeiro trade em minutos!
                    if current_price < Decimal(str(avg_price)) * Decimal('0.999'):  # 0.1% abaixo da média
                        # COMPRAR
                        try:
                            # Calcular quantidade baseada no capital
                            capital_per_trade = bot_config.capital / len(bot_config.symbols)
                            
                            # ✅ PYRAMIDING: Dividir capital entre posições
                            capital_per_position = capital_per_trade / MAX_POSITIONS
                            quantity = capital_per_position / current_price
                            
                            # Validar quantidade mínima
                            market = exchange.market(symbol)
                            min_qty = market['limits']['amount']['min'] or 0.001
                            if quantity < Decimal(str(min_qty)):
                                quantity = Decimal(str(min_qty))
                            
                            # Executar ordem de compra na exchange
                            order = exchange.create_market_order(symbol, 'buy', float(quantity))
                            
                            # CRIAR TRADE NO BANCO
                            Trade.objects.create(
                                user=bot_config.user,
                                bot_config=bot_config,
                                exchange=bot_config.exchange,
                                symbol=symbol,
                                side='buy',
                                entry_price=current_price,
                                quantity=quantity,
                                entry_time=timezone.now(),
                                status='open',
                                highest_price=current_price  # ✅ Iniciar trailing stop
                            )
                            
                            trades_executados += 1
                            print(f"🟢 COMPRA ({num_positions+1}/{MAX_POSITIONS}): {symbol} @ ${current_price:.2f} | Qtd: {quantity:.6f}")
                            
                        except Exception as e:
                            print(f"Erro ao abrir trade {symbol}: {e}")
            
        except Exception as e:
            print(f"Erro ao processar {symbol}: {e}")
    
    return f"Bot executado: {trades_executados} trades realizados em {len(bot_config.symbols)} símbolos"


# Tarefas periódicas
app.conf.beat_schedule = {
    'run-active-bots-every-second': {
        'task': 'saas.celery_config.check_active_bots',
        'schedule': 1.0,  # ✅ OTIMIZADO: A cada 1 segundo! (+400% oportunidades)
    },
}


@app.task
def check_active_bots():
    """Verifica quais bots estão ativos e executa"""
    from bots.models import BotConfiguration
    
    active_bots = BotConfiguration.objects.filter(is_active=True)
    
    for bot in active_bots:
        run_trading_bot.delay(bot.id)
    
    return f"{active_bots.count()} bots ativos"

