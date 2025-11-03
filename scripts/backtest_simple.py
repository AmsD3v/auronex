"""
Script simples para executar backtest (sem emojis para Windows)
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.exchange import BinanceExchange
from bot.strategies import TrendFollowingStrategy, MeanReversionStrategy
from bot.backtesting import BacktestEngine, BacktestVisualizer
from config.settings import Settings


def run_backtest(symbol: str = None, days: int = 30, strategy: str = None, 
                initial_capital: float = 10000):
    """Executa backtest"""
    settings = Settings()
    
    symbol = symbol or settings.TRADING_SYMBOL
    strategy_name = strategy or settings.STRATEGY
    
    print("\n" + "="*60)
    print("INICIANDO BACKTEST")
    print("="*60)
    print(f"\nSimbolo: {symbol}")
    print(f"Periodo: {days} dias")
    print(f"Estrategia: {strategy_name}")
    print(f"Capital Inicial: ${initial_capital:,.2f}\n")
    
    try:
        print("Conectando a Binance...")
        exchange = BinanceExchange()
        
        print(f"Obtendo {days} dias de dados historicos...")
        df = exchange.get_ohlcv(symbol, settings.TIMEFRAME, limit=days * 96)
        
        if df.empty:
            print("\nERRO: Nao foi possivel obter dados historicos\n")
            return False
        
        print(f"OK! {len(df)} candles obtidos\n")
        
        # Criar estratégia
        if strategy_name == 'trend_following':
            strategy_obj = TrendFollowingStrategy()
        elif strategy_name == 'mean_reversion':
            strategy_obj = MeanReversionStrategy()
        else:
            print(f"\nERRO: Estrategia desconhecida: {strategy_name}\n")
            return False
        
        print("Executando backtest...\n")
        engine = BacktestEngine(strategy_obj, initial_capital)
        results = engine.run(df)
        
        # Mostrar resultados
        print("\n" + "="*60)
        print("RESUMO DO BACKTEST")
        print("="*60)
        
        print("\n--- CAPITAL ---")
        print(f"Inicial:        ${results['initial_capital']:>15,.2f}")
        print(f"Final:          ${results['final_capital']:>15,.2f}")
        print(f"P&L Total:      ${results['total_pnl']:>15,.2f}")
        print(f"Retorno:        {results['total_return']:>15.2f}%")
        
        print("\n--- TRADES ---")
        print(f"Total:          {results['total_trades']:>15}")
        print(f"Vencedores:     {results['winning_trades']:>15}")
        print(f"Perdedores:     {results['losing_trades']:>15}")
        print(f"Taxa de Acerto: {results['win_rate']:>15.2f}%")
        
        print("\n--- MEDIAS ---")
        print(f"Ganho Medio:    ${results['avg_win']:>15.2f}")
        print(f"Perda Media:    ${results['avg_loss']:>15.2f}")
        print(f"Profit Factor:  {results['profit_factor']:>15.2f}")
        
        print("\n--- RISCO ---")
        print(f"Drawdown Max:   {results['max_drawdown']:>15.2f}%")
        print(f"Sharpe Ratio:   {results['sharpe_ratio']:>15.2f}")
        
        print("\n" + "="*60)
        
        # Análise
        print("\n--- ANALISE ---")
        win_rate = results['win_rate']
        profit_factor = results['profit_factor']
        total_return = results['total_return']
        
        if win_rate >= 60:
            print("  [OK] Excelente taxa de acerto!")
        elif win_rate >= 50:
            print("  [OK] Boa taxa de acerto")
        elif win_rate >= 40:
            print("  [!] Taxa de acerto razoavel")
        else:
            print("  [X] Taxa de acerto baixa")
        
        if profit_factor >= 2.0:
            print("  [OK] Excelente relacao lucro/perda")
        elif profit_factor >= 1.5:
            print("  [OK] Boa relacao lucro/perda")
        elif profit_factor >= 1.0:
            print("  [!] Relacao lucro/perda justa")
        else:
            print("  [X] Estrategia perdedora")
        
        if total_return >= 20:
            print("  [OK] Retorno excelente!")
        elif total_return >= 10:
            print("  [OK] Bom retorno")
        elif total_return >= 0:
            print("  [!] Retorno modesto")
        else:
            print("  [X] Retorno negativo")
        
        print("\n" + "="*60)
        
        # Visualizar
        visualizer = BacktestVisualizer(results)
        
        # Salvar relatório
        reports_dir = settings.BASE_DIR / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = reports_dir / f'backtest_{strategy_name}_{timestamp}.txt'
        
        visualizer.generate_report(report_file)
        print(f"\nRelatorio salvo em: {report_file}")
        
        # Gerar gráficos
        print("\nGerando graficos...")
        equity_chart = reports_dir / f'equity_{strategy_name}_{timestamp}.png'
        visualizer.plot_equity_curve(equity_chart)
        
        trades_chart = reports_dir / f'trades_{strategy_name}_{timestamp}.png'
        visualizer.plot_trades(df, trades_chart)
        
        print(f"Graficos salvos em: {reports_dir}\n")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\nERRO: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description='Executar backtest')
    parser.add_argument('--symbol', type=str, help='Par de trading')
    parser.add_argument('--days', type=int, default=30, help='Dias de historico')
    parser.add_argument('--strategy', type=str, choices=['trend_following', 'mean_reversion'],
                       help='Estrategia')
    parser.add_argument('--capital', type=float, default=10000, help='Capital inicial')
    
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








