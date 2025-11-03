"""
Busca TODAS as criptomoedas disponíveis na Binance
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange import BinanceExchange

def get_all_usdt_pairs():
    """Retorna todos os pares USDT da Binance"""
    
    print("\nBuscando todas as criptomoedas disponíveis na Binance...")
    
    exchange = BinanceExchange()
    
    # Carregar mercados
    markets = exchange.exchange.load_markets()
    
    # Filtrar apenas pares USDT
    usdt_pairs = []
    
    for symbol, info in markets.items():
        if symbol.endswith('/USDT'):
            # Converter formato CCXT (BTC/USDT) para Binance (BTCUSDT)
            binance_symbol = symbol.replace('/', '')
            usdt_pairs.append(binance_symbol)
    
    usdt_pairs.sort()
    
    print(f"\n Total de pares USDT: {len(usdt_pairs)}")
    print("\nPrimeiros 20:")
    for i, symbol in enumerate(usdt_pairs[:20], 1):
        print(f"  {i}. {symbol}")
    
    print(f"\n... e mais {len(usdt_pairs) - 20}!")
    
    # Salvar em arquivo
    with open('symbols_disponiveis.txt', 'w') as f:
        for symbol in usdt_pairs:
            f.write(f"{symbol}\n")
    
    print(f"\nLista completa salva em: symbols_disponiveis.txt")
    
    # Principais (mais conhecidas)
    principais = [s for s in usdt_pairs if any(x in s for x in [
        'BTC', 'ETH', 'BNB', 'SOL', 'ADA', 'XRP', 'DOGE', 
        'DOT', 'MATIC', 'AVAX', 'LINK', 'UNI', 'ATOM', 'LTC'
    ])]
    
    print(f"\nPrincipais ({len(principais)}):")
    for symbol in principais[:30]:
        print(f"  - {symbol}")
    
    return usdt_pairs

if __name__ == "__main__":
    symbols = get_all_usdt_pairs()





