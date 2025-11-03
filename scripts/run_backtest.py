"""
Script para executar backtesting
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange
from bot.strategies import TrendFollowingStrategy, MeanReversionStrategy
from bot.backtesting import BacktestEngine, BacktestVisualizer
from config.settings import Settings
from rich.console import Console

console = Console()


def run_backtest(symbol: str = None, days: int = 30, strategy: str = None, 
                initial_capital: float = 10000):
    """
    Executa backtest
    
    Args:
        symbol: Par de trading
        days: Número de dias de histórico
        strategy: Nome da estratégia
        initial_capital: Capital inicial
    """
    settings = Settings()
    
    # Usar valores padrão se não fornecidos
    symbol = symbol or settings.TRADING_SYMBOL
    strategy_name = strategy or settings.STRATEGY
    
    console.print("\n[bold cyan]📊 Iniciando Backtest...[/bold cyan]\n")
    console.print(f"Símbolo: [bold]{symbol}[/bold]")
    console.print(f"Período: [bold]{days} dias[/bold]")
    console.print(f"Estratégia: [bold]{strategy_name}[/bold]")
    console.print(f"Capital Inicial: [bold]${initial_capital:,.2f}[/bold]\n")
    
    try:
        # Conectar à exchange
        console.print("📡 Conectando à Binance...")
        exchange = BinanceExchange()
        
        # Baixar dados históricos
        console.print(f"📥 Baixando {days} dias de dados históricos...")
        df = exchange.get_ohlcv(symbol, settings.TIMEFRAME, limit=days * 96)  # ~96 candles de 15min por dia
        
        if df.empty:
            console.print("[bold red]❌ Não foi possível obter dados históricos[/bold red]\n")
            return False
        
        console.print(f"✅ {len(df)} candles obtidos\n")
        
        # Criar estratégia
        if strategy_name == 'trend_following':
            strategy_obj = TrendFollowingStrategy()
        elif strategy_name == 'mean_reversion':
            strategy_obj = MeanReversionStrategy()
        else:
            console.print(f"[bold red]❌ Estratégia desconhecida: {strategy_name}[/bold red]\n")
            return False
        
        # Executar backtest
        console.print("🔄 Executando backtest...\n")
        engine = BacktestEngine(strategy_obj, initial_capital)
        results = engine.run(df)
        
        # Visualizar resultados
        visualizer = BacktestVisualizer(results)
        visualizer.print_summary()
        visualizer.print_trades_list(limit=10)
        
        # Salvar relatório
        reports_dir = settings.BASE_DIR / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = reports_dir / f'backtest_{strategy_name}_{timestamp}.txt'
        
        report_text = visualizer.generate_report(report_file)
        console.print(f"\n💾 Relatório salvo em: [cyan]{report_file}[/cyan]")
        
        # Gerar gráficos
        console.print("\n📊 Gerando gráficos...")
        equity_chart = reports_dir / f'equity_{strategy_name}_{timestamp}.png'
        visualizer.plot_equity_curve(equity_chart)
        
        trades_chart = reports_dir / f'trades_{strategy_name}_{timestamp}.png'
        visualizer.plot_trades(df, trades_chart)
        
        console.print(f"✅ Gráficos salvos em: [cyan]{reports_dir}[/cyan]\n")
        
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Erro: {str(e)}[/bold red]\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Executar backtest de estratégia')
    parser.add_argument('--symbol', type=str, help='Par de trading (ex: BTCUSDT)')
    parser.add_argument('--days', type=int, default=30, help='Número de dias de histórico')
    parser.add_argument('--strategy', type=str, choices=['trend_following', 'mean_reversion'],
                       help='Estratégia a testar')
    parser.add_argument('--capital', type=float, default=10000, help='Capital inicial em USDT')
    
    args = parser.parse_args()
    
    success = run_backtest(
        symbol=args.symbol,
        days=args.days,
        strategy=args.strategy,
        initial_capital=args.capital
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

