"""
Roda o bot por 2 horas e salva resultados detalhados
"""

import sys
import time
import json
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from bot.exchange import BinanceExchange
from bot.risk_management import RiskManager
from bot.strategies import MeanReversionStrategy

def run_bot_2_hours():
    """Executa o bot por 2 horas"""
    
    settings = Settings()
    
    print("\n" + "="*70)
    print("BOT RODANDO - 2 HORAS")
    print("="*70)
    print(f"\nSimbolo: {settings.TRADING_SYMBOL}")
    print(f"Estrategia: {settings.STRATEGY}")
    print(f"Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print("\n" + "="*70 + "\n")
    
    # Arquivo de resultados
    results_file = Path('bot_2hours_results.json')
    
    try:
        exchange = BinanceExchange()
        risk_manager = RiskManager(exchange, None)
        risk_manager.initialize()
        strategy = MeanReversionStrategy()
        
        start_time = time.time()
        end_time = start_time + (2 * 60 * 60)  # 2 horas
        
        results = {
            'start_time': datetime.now().isoformat(),
            'symbol': settings.TRADING_SYMBOL,
            'strategy': settings.STRATEGY,
            'analyses': [],
            'signals': [],
            'prices': []
        }
        
        iteration = 0
        
        print("Bot iniciado! Salvando analises a cada minuto...\n")
        print("Para ver em tempo real, abra o dashboard:")
        print("  streamlit run dashboard.py\n")
        
        while time.time() < end_time:
            iteration += 1
            elapsed = int((time.time() - start_time) / 60)
            remaining = int((end_time - time.time()) / 60)
            
            print(f"[{iteration}] Tempo: {elapsed}min / {remaining}min restantes")
            
            try:
                df = exchange.get_ohlcv(settings.TRADING_SYMBOL, settings.TIMEFRAME, limit=100)
                
                if not df.empty:
                    signal = strategy.analyze(df)
                    current_price = df['close'].iloc[-1]
                    
                    # Registrar análise
                    analysis = {
                        'iteration': iteration,
                        'timestamp': datetime.now().isoformat(),
                        'price': float(current_price),
                        'signal': signal['signal'],
                        'confidence': float(signal['confidence']),
                        'reason': signal['reason']
                    }
                    
                    results['analyses'].append(analysis)
                    results['prices'].append(float(current_price))
                    
                    print(f"  Preco: ${current_price:,.2f}")
                    print(f"  Sinal: {signal['signal'].upper()} ({signal['confidence']:.1f}%)")
                    
                    # Se sinal forte, destacar
                    if signal['confidence'] >= 65:
                        results['signals'].append(analysis)
                        print(f"  >>> SINAL FORTE DETECTADO! <<<")
                        print(f"  {signal['reason']}")
                    
                    print()
                    
                    # Salvar resultados periodicamente
                    if iteration % 10 == 0:
                        with open(results_file, 'w', encoding='utf-8') as f:
                            json.dump(results, f, indent=2, ensure_ascii=False)
            
            except Exception as e:
                print(f"  Erro na iteracao: {e}")
            
            # Aguardar 1 minuto
            if time.time() < end_time:
                time.sleep(60)
        
        # Finalizar
        results['end_time'] = datetime.now().isoformat()
        results['duration_minutes'] = int((time.time() - start_time) / 60)
        
        # Estatísticas
        if results['prices']:
            results['stats'] = {
                'total_analyses': len(results['analyses']),
                'strong_signals': len(results['signals']),
                'initial_price': results['prices'][0],
                'final_price': results['prices'][-1],
                'price_variation': ((results['prices'][-1] - results['prices'][0]) / results['prices'][0]) * 100,
                'min_price': min(results['prices']),
                'max_price': max(results['prices'])
            }
        
        # Salvar final
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Mostrar resumo
        print("\n" + "="*70)
        print("TESTE DE 2 HORAS CONCLUIDO!")
        print("="*70 + "\n")
        
        stats = results.get('stats', {})
        print(f"Total de analises: {stats.get('total_analyses', 0)}")
        print(f"Sinais fortes: {stats.get('strong_signals', 0)}")
        print(f"Preco inicial: ${stats.get('initial_price', 0):,.2f}")
        print(f"Preco final: ${stats.get('final_price', 0):,.2f}")
        print(f"Variacao: {stats.get('price_variation', 0):+.2f}%")
        
        print(f"\nResultados salvos em: {results_file}")
        print("="*70 + "\n")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nBot interrompido pelo usuario.")
        
        # Salvar o que temos
        results['end_time'] = datetime.now().isoformat()
        results['interrupted'] = True
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados parciais salvos em: {results_file}")
        return False
    
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\nPara monitorar em tempo real, abra outro terminal e execute:")
    print("  streamlit run dashboard.py\n")
    print("Iniciando bot por 2 horas...\n")
    run_bot_2_hours()

