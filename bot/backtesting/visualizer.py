"""
Visualizador de Resultados do Backtesting
Gera gráficos e relatórios
"""

import logging
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class BacktestVisualizer:
    """
    Visualiza resultados de backtesting
    Gera gráficos e relatórios em texto
    """
    
    def __init__(self, results: Dict):
        """
        Inicializa o visualizador
        
        Args:
            results: Resultados do backtest
        """
        self.results = results
    
    def print_summary(self):
        """Imprime resumo dos resultados"""
        print("\n" + "="*60)
        print("📊 RESUMO DO BACKTEST")
        print("="*60)
        
        print(f"\n💰 CAPITAL:")
        print(f"  Inicial:        ${self.results['initial_capital']:,.2f}")
        print(f"  Final:          ${self.results['final_capital']:,.2f}")
        print(f"  P&L Total:      ${self.results['total_pnl']:+,.2f}")
        print(f"  Retorno:        {self.results['total_return']:+.2f}%")
        
        print(f"\n📈 TRADES:")
        print(f"  Total:          {self.results['total_trades']}")
        print(f"  Vencedores:     {self.results['winning_trades']} 🟢")
        print(f"  Perdedores:     {self.results['losing_trades']} 🔴")
        print(f"  Taxa de Acerto: {self.results['win_rate']:.2f}%")
        
        print(f"\n💵 MÉDIAS:")
        print(f"  Ganho Médio:    ${self.results['avg_win']:+,.2f}")
        print(f"  Perda Média:    ${self.results['avg_loss']:+,.2f}")
        print(f"  Profit Factor:  {self.results['profit_factor']:.2f}")
        
        print(f"\n📉 RISCO:")
        print(f"  Drawdown Máx:   {self.results['max_drawdown']:.2f}%")
        print(f"  Sharpe Ratio:   {self.results['sharpe_ratio']:.2f}")
        
        print("\n" + "="*60)
        
        # Análise qualitativa
        print("\n💡 ANÁLISE:")
        self.print_analysis()
        print("="*60 + "\n")
    
    def print_analysis(self):
        """Imprime análise qualitativa"""
        win_rate = self.results['win_rate']
        profit_factor = self.results['profit_factor']
        total_return = self.results['total_return']
        sharpe = self.results['sharpe_ratio']
        drawdown = self.results['max_drawdown']
        
        # Win Rate
        if win_rate >= 60:
            print("  ✅ Excelente taxa de acerto!")
        elif win_rate >= 50:
            print("  ✅ Boa taxa de acerto")
        elif win_rate >= 40:
            print("  ⚠️  Taxa de acerto razoável")
        else:
            print("  ❌ Taxa de acerto baixa")
        
        # Profit Factor
        if profit_factor >= 2.0:
            print("  ✅ Excelente relação lucro/perda")
        elif profit_factor >= 1.5:
            print("  ✅ Boa relação lucro/perda")
        elif profit_factor >= 1.0:
            print("  ⚠️  Relação lucro/perda justa")
        else:
            print("  ❌ Estratégia perdedora")
        
        # Retorno
        if total_return >= 20:
            print("  ✅ Retorno excelente!")
        elif total_return >= 10:
            print("  ✅ Bom retorno")
        elif total_return >= 0:
            print("  ⚠️  Retorno modesto")
        else:
            print("  ❌ Retorno negativo")
        
        # Drawdown
        if drawdown <= 10:
            print("  ✅ Drawdown controlado")
        elif drawdown <= 20:
            print("  ⚠️  Drawdown moderado")
        else:
            print("  ❌ Drawdown alto - risco elevado")
        
        # Sharpe Ratio
        if sharpe >= 2.0:
            print("  ✅ Excelente risco/retorno (Sharpe)")
        elif sharpe >= 1.0:
            print("  ✅ Bom risco/retorno (Sharpe)")
        elif sharpe >= 0:
            print("  ⚠️  Risco/retorno regular")
        else:
            print("  ❌ Risco/retorno ruim")
    
    def plot_equity_curve(self, save_path: Path = None):
        """
        Plota curva de equity
        
        Args:
            save_path: Caminho para salvar o gráfico
        """
        try:
            equity_df = pd.DataFrame(self.results['equity_curve'])
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
            
            # Gráfico 1: Equity
            ax1.plot(equity_df['timestamp'], equity_df['equity'], label='Equity', linewidth=2)
            ax1.axhline(y=self.results['initial_capital'], color='gray', linestyle='--', label='Capital Inicial')
            ax1.fill_between(equity_df['timestamp'], self.results['initial_capital'], equity_df['equity'],
                            where=(equity_df['equity'] >= self.results['initial_capital']), 
                            color='green', alpha=0.3)
            ax1.fill_between(equity_df['timestamp'], self.results['initial_capital'], equity_df['equity'],
                            where=(equity_df['equity'] < self.results['initial_capital']), 
                            color='red', alpha=0.3)
            ax1.set_title('Curva de Equity', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Capital (USDT)', fontsize=12)
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Drawdown
            equity_df['peak'] = equity_df['equity'].cummax()
            equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
            ax2.fill_between(equity_df['timestamp'], 0, equity_df['drawdown'], color='red', alpha=0.5)
            ax2.set_title('Drawdown', fontsize=14, fontweight='bold')
            ax2.set_ylabel('Drawdown (%)', fontsize=12)
            ax2.set_xlabel('Data', fontsize=12)
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"📊 Gráfico salvo em: {save_path}")
            else:
                plt.show()
            
            plt.close()
            
        except Exception as e:
            logger.error(f"Erro ao plotar equity curve: {e}")
    
    def plot_trades(self, df_price: pd.DataFrame, save_path: Path = None):
        """
        Plota trades no gráfico de preços
        
        Args:
            df_price: DataFrame com preços
            save_path: Caminho para salvar o gráfico
        """
        try:
            trades_df = pd.DataFrame(self.results['trades'])
            
            if trades_df.empty:
                logger.warning("Nenhum trade para plotar")
                return
            
            fig, ax = plt.subplots(figsize=(14, 6))
            
            # Plotar preços
            ax.plot(df_price.index, df_price['close'], label='Preço', linewidth=1.5, color='blue')
            
            # Plotar trades
            for _, trade in trades_df.iterrows():
                entry_time = trade['entry_time']
                exit_time = trade['exit_time']
                entry_price = trade['entry_price']
                exit_price = trade['exit_price']
                
                color = 'green' if trade['pnl'] > 0 else 'red'
                marker_entry = '^' if trade['side'] == 'long' else 'v'
                marker_exit = 'v' if trade['side'] == 'long' else '^'
                
                # Marcar entrada
                ax.scatter(entry_time, entry_price, color=color, marker=marker_entry, s=100, zorder=5)
                
                # Marcar saída
                ax.scatter(exit_time, exit_price, color=color, marker=marker_exit, s=100, zorder=5)
                
                # Linha conectando entrada e saída
                ax.plot([entry_time, exit_time], [entry_price, exit_price], 
                       color=color, linestyle='--', alpha=0.5, linewidth=1)
            
            ax.set_title('Trades no Gráfico de Preços', fontsize=14, fontweight='bold')
            ax.set_ylabel('Preço (USDT)', fontsize=12)
            ax.set_xlabel('Data', fontsize=12)
            ax.legend(['Preço', '↑ Compra', '↓ Venda'])
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"📊 Gráfico salvo em: {save_path}")
            else:
                plt.show()
            
            plt.close()
            
        except Exception as e:
            logger.error(f"Erro ao plotar trades: {e}")
    
    def print_trades_list(self, limit: int = 10):
        """
        Imprime lista de trades
        
        Args:
            limit: Número máximo de trades para mostrar
        """
        trades_df = pd.DataFrame(self.results['trades'])
        
        if trades_df.empty:
            print("\n⚠️  Nenhum trade executado")
            return
        
        print(f"\n📋 ÚLTIMOS {min(limit, len(trades_df))} TRADES:")
        print("-" * 100)
        
        for idx, trade in trades_df.tail(limit).iterrows():
            emoji = "💰" if trade['pnl'] > 0 else "❌"
            side_emoji = "🟢" if trade['side'] == 'long' else "🔴"
            
            print(f"{emoji} {side_emoji} {trade['side'].upper():5} | "
                  f"Entry: ${trade['entry_price']:8.2f} | "
                  f"Exit: ${trade['exit_price']:8.2f} | "
                  f"P&L: ${trade['pnl']:+8.2f} ({trade['pnl_percent']:+6.2f}%) | "
                  f"{trade['reason']}")
        
        print("-" * 100)
    
    def generate_report(self, save_path: Path = None) -> str:
        """
        Gera relatório completo em texto
        
        Args:
            save_path: Caminho para salvar o relatório
        
        Returns:
            String com o relatório
        """
        report = []
        report.append("="*80)
        report.append("RELATÓRIO DE BACKTEST - ROBOTRADER")
        report.append("="*80)
        report.append(f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        report.append(f"\n{'='*80}")
        
        # Capital
        report.append("\n1. RESUMO FINANCEIRO")
        report.append("-" * 80)
        report.append(f"Capital Inicial:      ${self.results['initial_capital']:>15,.2f}")
        report.append(f"Capital Final:        ${self.results['final_capital']:>15,.2f}")
        report.append(f"P&L Total:            ${self.results['total_pnl']:>15,.2f}")
        report.append(f"Retorno Total:        {self.results['total_return']:>15.2f}%")
        
        # Trades
        report.append(f"\n2. ESTATÍSTICAS DE TRADES")
        report.append("-" * 80)
        report.append(f"Total de Trades:      {self.results['total_trades']:>15}")
        report.append(f"Trades Vencedores:    {self.results['winning_trades']:>15}")
        report.append(f"Trades Perdedores:    {self.results['losing_trades']:>15}")
        report.append(f"Taxa de Acerto:       {self.results['win_rate']:>15.2f}%")
        report.append(f"Profit Factor:        {self.results['profit_factor']:>15.2f}")
        
        # Médias
        report.append(f"\n3. MÉDIAS")
        report.append("-" * 80)
        report.append(f"Ganho Médio:          ${self.results['avg_win']:>15.2f}")
        report.append(f"Perda Média:          ${self.results['avg_loss']:>15.2f}")
        
        # Risco
        report.append(f"\n4. MÉTRICAS DE RISCO")
        report.append("-" * 80)
        report.append(f"Drawdown Máximo:      {self.results['max_drawdown']:>15.2f}%")
        report.append(f"Sharpe Ratio:         {self.results['sharpe_ratio']:>15.2f}")
        
        report.append(f"\n{'='*80}\n")
        
        report_text = "\n".join(report)
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
            logger.info(f"📄 Relatório salvo em: {save_path}")
        
        return report_text

