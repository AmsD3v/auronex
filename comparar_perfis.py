"""
Compara os 4 perfis de trading com backtest
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange
from bot.strategies import MeanReversionStrategy
from bot.backtesting import BacktestEngine

# Perfis
PERFIS = {
    "Hedge Fund": {"tf": "1h", "sl": 0.02, "tp": 0.04},
    "Day Trader": {"tf": "15m", "sl": 0.015, "tp": 0.03},
    "Scalper": {"tf": "5m", "sl": 0.01, "tp": 0.02},
    "Ultra Scalper": {"tf": "1m", "sl": 0.005, "tp": 0.01}
}

def comparar():
    print("\n" + "="*80)
    print("COMPARACAO DE PERFIS - BACKTEST 30 DIAS")
    print("="*80 + "\n")
    
    exchange = BinanceExchange()
    strategy = MeanReversionStrategy()
    
    resultados = []
    
    for nome, config in PERFIS.items():
        print(f"\nTestando {nome}...")
        print(f"  Timeframe: {config['tf']} | SL: {config['sl']*100}% | TP: {config['tp']*100}%")
        
        try:
            # Obter dados
            df = exchange.get_ohlcv("ETHUSDT", config['tf'], limit=1000)
            
            # Criar engine com parâmetros do perfil
            engine = BacktestEngine(strategy, 10000)
            engine.stop_loss_percent = config['sl']
            engine.take_profit_percent = config['tp']
            
            # Executar
            results = engine.run(df)
            
            resultados.append({
                'perfil': nome,
                'timeframe': config['tf'],
                'trades': results['total_trades'],
                'win_rate': results['win_rate'],
                'retorno': results['total_return'],
                'profit_factor': results['profit_factor'],
                'drawdown': results['max_drawdown']
            })
            
            print(f"  OK - Trades: {results['total_trades']} | Win: {results['win_rate']:.1f}% | Retorno: {results['total_return']:+.2f}%")
            
        except Exception as e:
            print(f"  ERRO: {e}")
    
    # Resultados
    print("\n" + "="*80)
    print("RANKING - Melhor Retorno")
    print("="*80 + "\n")
    
    resultados.sort(key=lambda x: x['retorno'], reverse=True)
    
    print(f"{'#':<3} {'Perfil':<18} {'TF':<6} {'Trades':<8} {'Win%':<8} {'Retorno':<12} {'PF':<8} {'DD%':<8}")
    print("-" * 80)
    
    for i, r in enumerate(resultados, 1):
        medal = "[1]" if i == 1 else "[2]" if i == 2 else "[3]" if i == 3 else "   "
        print(f"{medal} {i} {r['perfil']:<18} {r['timeframe']:<6} {r['trades']:<8} {r['win_rate']:<7.1f}% {r['retorno']:>+10.2f}% {r['profit_factor']:<7.2f} {r['drawdown']:<7.2f}%")
    
    print("\n" + "="*80)
    print(f"\nCAMPEAO: {resultados[0]['perfil']}")
    print(f"Retorno: {resultados[0]['retorno']:+.2f}%")
    print(f"Trades: {resultados[0]['trades']}")
    print(f"Win Rate: {resultados[0]['win_rate']:.1f}%")
    print("="*80 + "\n")

if __name__ == "__main__":
    comparar()

