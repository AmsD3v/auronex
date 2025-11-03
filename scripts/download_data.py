"""
Script para baixar dados históricos
"""

import sys
import argparse
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange
from bot.data_manager import DataManager
from config.settings import Settings
from rich.console import Console
from rich.progress import Progress

console = Console()


def download_data(symbol: str = None, timeframe: str = None, days: int = 30):
    """
    Baixa dados históricos e salva no banco
    
    Args:
        symbol: Par de trading
        timeframe: Período dos candles
        days: Número de dias de histórico
    """
    settings = Settings()
    
    # Usar valores padrão
    symbol = symbol or settings.TRADING_SYMBOL
    timeframe = timeframe or settings.TIMEFRAME
    
    console.print("\n[bold cyan]📥 Baixando Dados Históricos...[/bold cyan]\n")
    console.print(f"Símbolo: [bold]{symbol}[/bold]")
    console.print(f"Timeframe: [bold]{timeframe}[/bold]")
    console.print(f"Período: [bold]{days} dias[/bold]\n")
    
    try:
        # Conectar à exchange
        console.print("📡 Conectando à Binance...")
        exchange = BinanceExchange()
        
        # Criar data manager
        data_manager = DataManager(exchange)
        
        # Baixar dados
        console.print(f"\n📥 Baixando dados...")
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Baixando...", total=100)
            
            df = data_manager.download_historical_data(symbol, timeframe, days)
            
            progress.update(task, completed=100)
        
        if df.empty:
            console.print("[bold red]❌ Nenhum dado foi baixado[/bold red]\n")
            return False
        
        # Resumo
        console.print(f"\n[bold green]✅ Download concluído![/bold green]")
        console.print(f"\n📊 Resumo:")
        console.print(f"  Total de candles: [bold]{len(df)}[/bold]")
        console.print(f"  Período: [bold]{df.index[0]} até {df.index[-1]}[/bold]")
        console.print(f"  Preço inicial: [green]${df['close'].iloc[0]:.2f}[/green]")
        console.print(f"  Preço final: [green]${df['close'].iloc[-1]:.2f}[/green]")
        
        variation = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
        color = "green" if variation > 0 else "red"
        console.print(f"  Variação: [{color}]{variation:+.2f}%[/{color}]\n")
        
        # Localização do banco
        console.print(f"💾 Dados salvos em: [cyan]{data_manager.db_path}[/cyan]\n")
        
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Erro: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Baixar dados históricos')
    parser.add_argument('--symbol', type=str, help='Par de trading (ex: BTCUSDT)')
    parser.add_argument('--timeframe', type=str, help='Timeframe (ex: 1m, 5m, 15m, 1h)')
    parser.add_argument('--days', type=int, default=30, help='Número de dias de histórico')
    
    args = parser.parse_args()
    
    success = download_data(
        symbol=args.symbol,
        timeframe=args.timeframe,
        days=args.days
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

