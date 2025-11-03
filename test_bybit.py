"""
Teste de conexão com Bybit
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bot.exchange_multi import MultiExchange

def test_bybit():
    print("\n" + "="*70)
    print("TESTANDO CONEXÃO BYBIT")
    print("="*70 + "\n")
    
    try:
        # Conectar
        print("Conectando à Bybit Testnet...")
        exchange = MultiExchange("Bybit")
        
        # Testar saldo
        print("\nObtendo saldo...")
        saldo_usdt = exchange.get_usdt_balance()
        print(f"Saldo USDT: ${saldo_usdt:,.2f}")
        
        # Testar ticker
        print("\nObtendo preço Bitcoin...")
        ticker = exchange.get_ticker('BTCUSDT')
        
        if ticker:
            print(f"BTC: ${ticker['last']:,.2f}")
            print(f"24h High: ${ticker['high']:,.2f}")
            print(f"24h Low: ${ticker['low']:,.2f}")
        
        # Testar OHLCV
        print("\nObtendo dados históricos...")
        df = exchange.get_ohlcv('BTCUSDT', '15m', limit=10)
        
        if not df.empty:
            print(f"Candles obtidos: {len(df)}")
            print(f"Último preço: ${df['close'].iloc[-1]:,.2f}")
        
        print("\n" + "="*70)
        print("BYBIT FUNCIONANDO PERFEITAMENTE! ✅")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\nERRO: {e}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_bybit()



