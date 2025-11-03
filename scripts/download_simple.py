"""
Script simples para baixar dados (sem emojis para Windows)
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange
from bot.data_manager import DataManager
from config.settings import Settings


def download_data(symbol: str = None, timeframe: str = None, days: int = 30):
    """Baixa dados históricos"""
    settings = Settings()
    
    symbol = symbol or settings.TRADING_SYMBOL
    timeframe = timeframe or settings.TIMEFRAME
    
    print("\n" + "="*60)
    print("BAIXANDO DADOS HISTORICOS")
    print("="*60)
    print(f"\nSimbolo: {symbol}")
    print(f"Timeframe: {timeframe}")
    print(f"Periodo: {days} dias\n")
    
    try:
        print("Conectando a Binance...")
        exchange = BinanceExchange()
        
        data_manager = DataManager(exchange)
        
        print(f"Baixando {days} dias de dados...")
        df = data_manager.download_historical_data(symbol, timeframe, days)
        
        if df.empty:
            print("\nERRO: Nenhum dado foi baixado\n")
            return False
        
        print("\n" + "="*60)
        print("DOWNLOAD CONCLUIDO!")
        print("="*60)
        print(f"\nTotal de candles: {len(df)}")
        print(f"Periodo: {df.index[0]} ate {df.index[-1]}")
        print(f"Preco inicial: ${df['close'].iloc[0]:.2f}")
        print(f"Preco final: ${df['close'].iloc[-1]:.2f}")
        
        variation = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
        print(f"Variacao: {variation:+.2f}%")
        
        print(f"\nDados salvos em: {data_manager.db_path}")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\nERRO: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description='Baixar dados históricos')
    parser.add_argument('--symbol', type=str, help='Par de trading (ex: BTCUSDT)')
    parser.add_argument('--timeframe', type=str, help='Timeframe (ex: 1m, 5m, 15m, 1h)')
    parser.add_argument('--days', type=int, default=30, help='Número de dias')
    
    args = parser.parse_args()
    
    success = download_data(
        symbol=args.symbol,
        timeframe=args.timeframe,
        days=args.days
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()








