"""
Engine de Backtesting
Testa estratégias com dados históricos
"""

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from config.settings import Settings

logger = logging.getLogger(__name__)


class BacktestEngine:
    """
    Motor de backtesting para testar estratégias
    Simula trading com dados históricos
    """
    
    def __init__(self, strategy, initial_capital: float = None):
        """
        Inicializa o engine de backtesting
        
        Args:
            strategy: Instância da estratégia a ser testada
            initial_capital: Capital inicial (USDT)
        """
        self.strategy = strategy
        self.settings = Settings()
        self.initial_capital = initial_capital or self.settings.BACKTEST_INITIAL_CAPITAL
        
        # Estado
        self.capital = self.initial_capital
        self.position = None  # None, 'long' ou 'short'
        self.position_size = 0
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.highest_price = 0  # Para trailing stop
        
        # Resultados
        self.trades = []
        self.equity_curve = []
        self.daily_returns = []
        
        # Configurações
        self.commission = self.settings.BACKTEST_COMMISSION
        self.stop_loss_percent = self.settings.STOP_LOSS_PERCENT
        self.take_profit_percent = self.settings.TAKE_PROFIT_PERCENT
    
    def run(self, df: pd.DataFrame) -> Dict:
        """
        Executa o backtest
        
        Args:
            df: DataFrame com dados históricos OHLCV
        
        Returns:
            Dicionário com resultados do backtest
        """
        logger.info(f"🔄 Iniciando backtest com {len(df)} candles...")
        logger.info(f"Capital inicial: ${self.initial_capital:.2f}")
        logger.info(f"Estratégia: {self.strategy.get_name()}")
        
        # Reset do estado
        self.capital = self.initial_capital
        self.position = None
        self.trades = []
        self.equity_curve = []
        
        # Iterar por cada candle
        for i in range(50, len(df)):  # Começar após 50 candles (para indicadores)
            current_df = df.iloc[:i+1]
            current_candle = df.iloc[i]
            current_price = current_candle['close']
            timestamp = current_candle.name
            
            # Registrar equity
            current_equity = self.calculate_current_equity(current_price)
            self.equity_curve.append({
                'timestamp': timestamp,
                'equity': current_equity,
                'capital': self.capital,
                'position': self.position
            })
            
            # Se estiver em posição, verificar stop loss / take profit
            if self.position:
                self.check_exit_conditions(current_price, timestamp)
            
            # Se não estiver em posição, procurar entrada
            if not self.position:
                signal = self.strategy.analyze(current_df)
                
                if signal['signal'] == 'buy' and signal['confidence'] > 60:
                    self.enter_long(current_price, timestamp, signal)
                
                elif signal['signal'] == 'sell' and signal['confidence'] > 60:
                    self.enter_short(current_price, timestamp, signal)
            
            # Se estiver em posição, verificar sinal de saída da estratégia
            else:
                should_exit, reason = self.strategy.should_exit_position(
                    current_df, 
                    'buy' if self.position == 'long' else 'sell'
                )
                
                if should_exit:
                    self.exit_position(current_price, timestamp, reason)
        
        # Fechar posição aberta ao final
        if self.position:
            final_price = df.iloc[-1]['close']
            final_timestamp = df.iloc[-1].name
            self.exit_position(final_price, final_timestamp, "Fim do backtest")
        
        # Calcular métricas
        results = self.calculate_metrics()
        
        logger.info(f"✅ Backtest concluído!")
        logger.info(f"Total de trades: {results['total_trades']}")
        logger.info(f"Win rate: {results['win_rate']:.2f}%")
        logger.info(f"Retorno total: {results['total_return']:.2f}%")
        logger.info(f"Capital final: ${results['final_capital']:.2f}")
        
        return results
    
    def enter_long(self, price: float, timestamp, signal: Dict):
        """Entra em posição comprada"""
        # Calcular tamanho da posição
        position_value = self.capital * self.settings.POSITION_SIZE_PERCENT
        self.position_size = position_value / price
        
        # Aplicar comissão
        commission_cost = position_value * self.commission
        self.capital -= commission_cost
        
        # Definir stop loss e take profit
        self.entry_price = price
        self.stop_loss = price * (1 - self.stop_loss_percent)
        self.take_profit = price * (1 + self.take_profit_percent)
        self.highest_price = price
        
        self.position = 'long'
        
        logger.debug(f"📈 LONG @ ${price:.2f} | Size: {self.position_size:.6f} | SL: ${self.stop_loss:.2f} | TP: ${self.take_profit:.2f}")
    
    def enter_short(self, price: float, timestamp, signal: Dict):
        """Entra em posição vendida"""
        # Calcular tamanho da posição
        position_value = self.capital * self.settings.POSITION_SIZE_PERCENT
        self.position_size = position_value / price
        
        # Aplicar comissão
        commission_cost = position_value * self.commission
        self.capital -= commission_cost
        
        # Definir stop loss e take profit
        self.entry_price = price
        self.stop_loss = price * (1 + self.stop_loss_percent)
        self.take_profit = price * (1 - self.take_profit_percent)
        self.highest_price = price
        
        self.position = 'short'
        
        logger.debug(f"📉 SHORT @ ${price:.2f} | Size: {self.position_size:.6f} | SL: ${self.stop_loss:.2f} | TP: ${self.take_profit:.2f}")
    
    def exit_position(self, price: float, timestamp, reason: str):
        """Sai da posição atual"""
        if not self.position:
            return
        
        # Calcular P&L
        if self.position == 'long':
            pnl = (price - self.entry_price) * self.position_size
            pnl_percent = ((price - self.entry_price) / self.entry_price) * 100
        else:  # short
            pnl = (self.entry_price - price) * self.position_size
            pnl_percent = ((self.entry_price - price) / self.entry_price) * 100
        
        # Aplicar comissão de saída
        exit_value = price * self.position_size
        commission_cost = exit_value * self.commission
        pnl -= commission_cost
        
        # Atualizar capital
        self.capital += pnl
        
        # Registrar trade
        trade = {
            'entry_time': timestamp,
            'exit_time': timestamp,
            'side': self.position,
            'entry_price': self.entry_price,
            'exit_price': price,
            'size': self.position_size,
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'reason': reason,
            'capital_after': self.capital
        }
        self.trades.append(trade)
        
        emoji = "💰" if pnl > 0 else "❌"
        logger.debug(f"{emoji} EXIT @ ${price:.2f} | P&L: ${pnl:.2f} ({pnl_percent:+.2f}%) | Motivo: {reason}")
        
        # Reset
        self.position = None
        self.position_size = 0
        self.entry_price = 0
    
    def check_exit_conditions(self, current_price: float, timestamp):
        """Verifica se deve sair por stop loss ou take profit"""
        if not self.position:
            return
        
        if self.position == 'long':
            # Atualizar preço mais alto (para trailing stop)
            if current_price > self.highest_price:
                self.highest_price = current_price
                # Atualizar trailing stop
                if self.settings.USE_TRAILING_STOP:
                    new_stop = current_price * (1 - self.settings.TRAILING_STOP_PERCENT)
                    if new_stop > self.stop_loss:
                        self.stop_loss = new_stop
            
            # Verificar stop loss
            if current_price <= self.stop_loss:
                self.exit_position(current_price, timestamp, "Stop Loss")
                return
            
            # Verificar take profit
            if current_price >= self.take_profit:
                self.exit_position(current_price, timestamp, "Take Profit")
                return
        
        else:  # short
            # Atualizar preço mais baixo (para trailing stop)
            if current_price < self.highest_price:
                self.highest_price = current_price
                # Atualizar trailing stop
                if self.settings.USE_TRAILING_STOP:
                    new_stop = current_price * (1 + self.settings.TRAILING_STOP_PERCENT)
                    if new_stop < self.stop_loss:
                        self.stop_loss = new_stop
            
            # Verificar stop loss
            if current_price >= self.stop_loss:
                self.exit_position(current_price, timestamp, "Stop Loss")
                return
            
            # Verificar take profit
            if current_price <= self.take_profit:
                self.exit_position(current_price, timestamp, "Take Profit")
                return
    
    def calculate_current_equity(self, current_price: float) -> float:
        """Calcula equity atual (capital + posição aberta)"""
        if not self.position:
            return self.capital
        
        if self.position == 'long':
            unrealized_pnl = (current_price - self.entry_price) * self.position_size
        else:
            unrealized_pnl = (self.entry_price - current_price) * self.position_size
        
        return self.capital + unrealized_pnl
    
    def calculate_metrics(self) -> Dict:
        """Calcula métricas de performance"""
        if not self.trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_return': 0,
                'final_capital': self.capital,
                'max_drawdown': 0,
                'sharpe_ratio': 0,
                'profit_factor': 0,
            }
        
        # Trades
        trades_df = pd.DataFrame(self.trades)
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df['pnl'] > 0])
        losing_trades = len(trades_df[trades_df['pnl'] < 0])
        
        # Win rate
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # Retorno total
        total_return = ((self.capital - self.initial_capital) / self.initial_capital) * 100
        
        # Profit factor (total lucro / total perda)
        total_profit = trades_df[trades_df['pnl'] > 0]['pnl'].sum()
        total_loss = abs(trades_df[trades_df['pnl'] < 0]['pnl'].sum())
        profit_factor = (total_profit / total_loss) if total_loss > 0 else float('inf')
        
        # Drawdown
        equity_df = pd.DataFrame(self.equity_curve)
        equity_df['peak'] = equity_df['equity'].cummax()
        equity_df['drawdown'] = (equity_df['equity'] - equity_df['peak']) / equity_df['peak'] * 100
        max_drawdown = abs(equity_df['drawdown'].min())
        
        # Sharpe Ratio (simplificado)
        returns = equity_df['equity'].pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        # Trade médio
        avg_win = trades_df[trades_df['pnl'] > 0]['pnl'].mean() if winning_trades > 0 else 0
        avg_loss = trades_df[trades_df['pnl'] < 0]['pnl'].mean() if losing_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'initial_capital': self.initial_capital,
            'final_capital': self.capital,
            'total_pnl': self.capital - self.initial_capital,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'profit_factor': profit_factor,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'trades': self.trades,
            'equity_curve': self.equity_curve,
        }

