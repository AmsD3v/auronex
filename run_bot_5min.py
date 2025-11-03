"""
Roda o bot por 5 minutos e mostra resultados
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path

# Configurar logging simples
log_file = Path('bot_5min_test.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Imports do bot
from config.settings import Settings
from bot.exchange import BinanceExchange
from bot.risk_management import RiskManager
from bot.data_manager import DataManager
from bot.strategies import MeanReversionStrategy

def run_bot_for_5min():
    """Executa o bot por 5 minutos"""
    
    settings = Settings()
    
    print("\n" + "="*70)
    print("BOT RODANDO EM TEMPO REAL - 5 MINUTOS")
    print("="*70)
    print(f"\nSimbolo: {settings.TRADING_SYMBOL}")
    print(f"Estrategia: {settings.STRATEGY}")
    print(f"Timeframe: {settings.TIMEFRAME}")
    print(f"Modo: TESTNET (Paper Trading)")
    print(f"Duracao: 5 minutos")
    print("\n" + "="*70 + "\n")
    
    try:
        # Inicializar componentes
        print("Inicializando...")
        exchange = BinanceExchange()
        risk_manager = RiskManager(exchange, None)
        risk_manager.initialize()
        strategy = MeanReversionStrategy()
        
        print(f"Saldo inicial: ${exchange.get_usdt_balance():.2f} USDT\n")
        
        # Tempo de execução
        start_time = time.time()
        end_time = start_time + (5 * 60)  # 5 minutos
        
        iteration = 0
        signals_found = []
        
        print("Bot iniciado! Analisando mercado a cada 30 segundos...\n")
        
        while time.time() < end_time:
            iteration += 1
            remaining = int((end_time - time.time()) / 60)
            
            print(f"[{iteration}] Tempo restante: {remaining} minutos...")
            
            # Obter dados
            df = exchange.get_ohlcv(settings.TRADING_SYMBOL, settings.TIMEFRAME, limit=100)
            
            if not df.empty:
                # Analisar
                signal = strategy.analyze(df)
                
                current_price = df['close'].iloc[-1]
                
                print(f"  Preco atual: ${current_price:,.2f}")
                print(f"  Sinal: {signal['signal'].upper()}")
                print(f"  Confianca: {signal['confidence']:.1f}%")
                print(f"  Motivo: {signal['reason']}")
                
                # Se sinal forte, registrar
                if signal['confidence'] >= 65:
                    signal_data = {
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'signal': signal['signal'],
                        'price': current_price,
                        'confidence': signal['confidence'],
                        'reason': signal['reason']
                    }
                    signals_found.append(signal_data)
                    
                    if signal['signal'] == 'buy':
                        print("  >>> OPORTUNIDADE DE COMPRA DETECTADA! <<<")
                    elif signal['signal'] == 'sell':
                        print("  >>> OPORTUNIDADE DE VENDA DETECTADA! <<<")
                
                print()
            
            # Aguardar 30 segundos
            if time.time() < end_time:
                time.sleep(30)
        
        # Resultados finais
        print("\n" + "="*70)
        print("TESTE DE 5 MINUTOS CONCLUIDO!")
        print("="*70 + "\n")
        
        print(f"Total de analises: {iteration}")
        print(f"Sinais fortes encontrados: {len(signals_found)}")
        
        if signals_found:
            print("\n--- SINAIS DETECTADOS ---")
            for s in signals_found:
                emoji = "BUY" if s['signal'] == 'buy' else "SELL"
                print(f"  [{s['time']}] {emoji} @ ${s['price']:,.2f} - {s['reason']} (Conf: {s['confidence']:.1f}%)")
        else:
            print("\nNenhum sinal forte detectado no periodo.")
            print("Isso e NORMAL - a estrategia e seletiva!")
        
        print(f"\nSaldo final: ${exchange.get_usdt_balance():.2f} USDT")
        print("\n" + "="*70)
        print("\nNOTA: Este foi um teste de observacao.")
        print("Paper Trading estava ativo - nenhuma ordem foi executada.")
        print("="*70 + "\n")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nBot interrompido pelo usuario.")
        return False
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    run_bot_for_5min()








