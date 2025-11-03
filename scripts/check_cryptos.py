"""
Verificar performance de criptomoedas
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange


def check():
    print("\n" + "="*70)
    print("PERFORMANCE RECENTE DAS CRIPTOMOEDAS")
    print("="*70 + "\n")
    
    exchange = BinanceExchange()
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'DOGEUSDT']
    
    results = []
    
    for symbol in symbols:
        try:
            # Pegar dados recentes (timeframe 15m, últimos 30 dias = ~2880 candles)
            df = exchange.get_ohlcv(symbol, '15m', limit=1000)
            
            if not df.empty:
                initial = df['close'].iloc[0]
                final = df['close'].iloc[-1]
                var = ((final - initial) / initial) * 100
                
                # Volatilidade
                vol = df['close'].pct_change().std() * 100
                
                results.append({
                    'symbol': symbol,
                    'initial': initial,
                    'final': final,
                    'var': var,
                    'vol': vol
                })
                
                status = "OK" if var > 0 else "Negativo"
                print(f"{symbol:<12} Inicial: ${initial:>10,.2f}  Final: ${final:>10,.2f}  Var: {var:>7.2f}%  [{status}]")
                
        except Exception as e:
            print(f"{symbol:<12} ERRO: {e}")
    
    if results:
        print("\n" + "="*70)
        print("RANKING")
        print("="*70)
        
        # Ordenar por variação
        results.sort(key=lambda x: x['var'], reverse=True)
        
        print(f"\n{'#':<3} {'Simbolo':<12} {'Variacao':>12} {'Volatilidade':>15}")
        print("-" * 70)
        
        for i, r in enumerate(results, 1):
            print(f"{i:<3} {r['symbol']:<12} {r['var']:>11.2f}% {r['vol']:>14.2f}%")
        
        best = results[0]
        most_vol = max(results, key=lambda x: x['vol'])
        
        print("\n" + "="*70)
        print(f"MELHOR RETORNO: {best['symbol']} ({best['var']:+.2f}%)")
        print(f"MAIS VOLATIL: {most_vol['symbol']} ({most_vol['vol']:.2f}% vol)")
        print("="*70 + "\n")
        
        print("Recomendacao:")
        print(f"  -> Para Trend Following: {best['symbol']} (melhor tendencia)")
        print(f"  -> Para Mean Reversion: {most_vol['symbol']} (mais oscilacoes)")
        print()

if __name__ == "__main__":
    check()








