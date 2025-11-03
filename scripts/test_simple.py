"""
Script simples para testar conexão (sem emojis para Windows)
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange
from config.settings import Settings


def test_connection():
    """Testa conexão com Binance"""
    print("\n" + "="*60)
    print("TESTANDO CONEXAO COM BINANCE")
    print("="*60 + "\n")
    
    settings = Settings()
    
    # Mostrar modo
    mode = "TESTNET" if settings.USE_TESTNET else "PRODUCAO"
    print(f"Modo: {mode}\n")
    
    try:
        # Criar exchange
        print("Conectando...")
        exchange = BinanceExchange()
        
        # Testar conexão
        ticker = exchange.get_ticker(settings.TRADING_SYMBOL)
        balance = exchange.get_balance()
        
        if ticker and balance:
            print("\n" + "="*60)
            print("CONEXAO OK!")
            print("="*60)
            
            # Informações básicas
            print(f"\nSimbolo: {settings.TRADING_SYMBOL}")
            print(f"Preco Atual: ${ticker['last']:,.2f}")
            
            # Saldo
            print(f"\n--- SALDOS ---")
            for coin in ['USDT', 'BTC', 'ETH', 'BNB']:
                if coin in balance:
                    total = balance[coin]['total']
                    if total > 0:
                        print(f"{coin}: {total:.8f}")
            
            # Info de mercado
            print(f"\n--- MERCADO (24h) ---")
            print(f"High: ${ticker['high']:,.2f}")
            print(f"Low: ${ticker['low']:,.2f}")
            print(f"Volume: {ticker['baseVolume']:,.2f}")
            
            print("\n" + "="*60)
            print("SUCESSO! Tudo funcionando!")
            print("="*60 + "\n")
            
            return True
        else:
            print("\nERRO: Nao foi possivel obter dados")
            return False
            
    except Exception as e:
        print(f"\nERRO: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)








