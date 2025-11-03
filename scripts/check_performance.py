"""
Script para verificar performance de várias criptomoedas
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange
from config.settings import Settings


def check_performance():
    """Verifica performance das principais criptos"""
    
    # Principais criptomoedas
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'DOGEUSDT', 'AVAXUSDT', 'DOTUSDT']
    
    print("\n" + "="*80)
    print("PERFORMANCE DAS PRINCIPAIS CRIPTOMOEDAS - ULTIMOS 90 DIAS")
    print("="*80 + "\n")
    
    try:
        exchange = BinanceExchange()
        results = []
        
        for symbol in symbols:
            try:
                # Pegar dados de 90 dias (aproximadamente)
                df = exchange.get_ohlcv(symbol, '1d', limit=90)
                
                if not df.empty and len(df) >= 30:
                    initial_price = df['close'].iloc[0]
                    final_price = df['close'].iloc[-1]
                    variation = ((final_price - initial_price) / initial_price) * 100
                    
                    # Calcular volatilidade
                    volatility = df['close'].pct_change().std() * 100
                    
                    results.append({
                        'symbol': symbol,
                        'initial': initial_price,
                        'final': final_price,
                        'variation': variation,
                        'volatility': volatility,
                        'days': len(df)
                    })
                    
                    print(f"Analisando {symbol}... OK")
                else:
                    print(f"Analisando {symbol}... Dados insuficientes")
                    
            except Exception as e:
                print(f"Analisando {symbol}... Erro: {e}")
                continue
        
        if not results:
            print("\nERRO: Nenhum dado obtido")
            return
        
        # Ordenar por variação (melhor performance)
        results.sort(key=lambda x: x['variation'], reverse=True)
        
        print("\n" + "="*80)
        print("RANKING - Melhores Performances")
        print("="*80 + "\n")
        
        print(f"{'#':<3} {'Simbolo':<12} {'Preco Inicial':>15} {'Preco Final':>15} {'Variacao':>12} {'Volatilidade':>12}")
        print("-" * 80)
        
        for i, r in enumerate(results, 1):
            emoji = "🟢" if r['variation'] > 0 else "🔴"
            print(f"{i:<3} {r['symbol']:<12} ${r['initial']:>14,.2f} ${r['final']:>14,.2f} {r['variation']:>11.2f}% {r['volatility']:>11.2f}%")
        
        print("\n" + "="*80)
        
        # Melhor para trading
        best = results[0]
        print(f"\nMELHOR PERFORMANCE: {best['symbol']}")
        print(f"Variacao: {best['variation']:+.2f}%")
        print(f"Volatilidade: {best['volatility']:.2f}% (quanto maior, mais oportunidades)")
        
        # Mais volátil
        most_volatile = max(results, key=lambda x: x['volatility'])
        print(f"\nMAIS VOLATIL: {most_volatile['symbol']}")
        print(f"Volatilidade: {most_volatile['volatility']:.2f}%")
        print(f"Variacao: {most_volatile['variation']:+.2f}%")
        
        print("\n" + "="*80)
        print("\nRecomendacao para Trading:")
        print(f"- Melhor Retorno: {best['symbol']} ({best['variation']:+.2f}%)")
        print(f"- Mais Oportunidades: {most_volatile['symbol']} ({most_volatile['volatility']:.2f}% volatilidade)")
        print("="*80 + "\n")
        
        return results
        
    except Exception as e:
        print(f"\nERRO: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_performance()








