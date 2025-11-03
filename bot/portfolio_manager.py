"""
Gerenciador de Portfolio Multi-Cripto
Gerencia múltiplas criptomoedas simultaneamente
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from config.settings import Settings

logger = logging.getLogger(__name__)


class PortfolioManager:
    """
    Gerenciador de portfolio multi-cripto
    - Divide capital entre múltiplas criptomoedas
    - Gerencia posições simultâneas
    - Otimiza alocação
    """
    
    def __init__(self, exchange, risk_manager, data_manager):
        """Inicializa o gerenciador de portfolio"""
        self.settings = Settings()
        self.exchange = exchange
        self.risk_manager = risk_manager
        self.data_manager = data_manager
        
        # Criptos para monitorar
        self.symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
        
        # Posições abertas por símbolo
        self.positions = {}  # {symbol: {entry_price, quantity, stop_loss, take_profit}}
        
        # Capital alocado por símbolo
        self.capital_allocation = {}
        
        # Total de capital
        self.total_capital = 0
        self.initial_capital = 0
    
    def initialize(self, total_capital: float = None):
        """
        Inicializa o portfolio
        
        Args:
            total_capital: Capital total para dividir (se None, usa saldo disponível)
        """
        if total_capital:
            self.total_capital = total_capital
        else:
            self.total_capital = self.exchange.get_usdt_balance()
        
        self.initial_capital = self.total_capital
        
        # Dividir capital igualmente entre símbolos
        capital_por_cripto = self.total_capital / len(self.symbols)
        
        for symbol in self.symbols:
            self.capital_allocation[symbol] = capital_por_cripto
        
        logger.info(f"Portfolio inicializado com ${self.total_capital:.2f}")
        logger.info(f"Capital por cripto: ${capital_por_cripto:.2f}")
    
    def get_available_capital(self, symbol: str) -> float:
        """Retorna capital disponível para um símbolo"""
        # Se já está em posição, não tem capital disponível
        if symbol in self.positions:
            return 0.0
        
        return self.capital_allocation.get(symbol, 0.0)
    
    def open_position(self, symbol: str, entry_price: float, quantity: float,
                     stop_loss: float, take_profit: float, order_id: str = None):
        """Abre uma posição"""
        self.positions[symbol] = {
            'entry_price': entry_price,
            'quantity': quantity,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'order_id': order_id,
            'entry_time': datetime.now(),
            'highest_price': entry_price
        }
        
        logger.info(f"Posicao aberta em {symbol} @ ${entry_price:.2f}")
    
    def close_position(self, symbol: str, exit_price: float, reason: str) -> Dict:
        """
        Fecha uma posição
        
        Returns:
            Dicionário com informações do trade fechado
        """
        if symbol not in self.positions:
            return {}
        
        position = self.positions[symbol]
        
        # Calcular P&L
        pnl = (exit_price - position['entry_price']) * position['quantity']
        pnl_percent = ((exit_price - position['entry_price']) / position['entry_price']) * 100
        
        trade_result = {
            'symbol': symbol,
            'entry_price': position['entry_price'],
            'exit_price': exit_price,
            'quantity': position['quantity'],
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'reason': reason,
            'duration': (datetime.now() - position['entry_time']).total_seconds() / 60
        }
        
        # Remover posição
        del self.positions[symbol]
        
        logger.info(f"Posicao fechada em {symbol}: P&L ${pnl:+.2f} ({pnl_percent:+.2f}%)")
        
        return trade_result
    
    def get_position(self, symbol: str) -> Optional[Dict]:
        """Retorna posição de um símbolo"""
        return self.positions.get(symbol, None)
    
    def has_position(self, symbol: str) -> bool:
        """Verifica se tem posição aberta em um símbolo"""
        return symbol in self.positions
    
    def get_all_positions(self) -> Dict:
        """Retorna todas as posições abertas"""
        return self.positions.copy()
    
    def get_total_positions(self) -> int:
        """Retorna número de posições abertas"""
        return len(self.positions)
    
    def calculate_portfolio_value(self, current_prices: Dict[str, float]) -> Dict:
        """
        Calcula valor atual do portfolio
        
        Args:
            current_prices: {symbol: price}
        
        Returns:
            Dicionário com métricas do portfolio
        """
        total_value = 0
        unrealized_pnl = 0
        
        # Capital não usado
        for symbol in self.symbols:
            if symbol not in self.positions:
                total_value += self.capital_allocation.get(symbol, 0)
        
        # Posições abertas
        for symbol, position in self.positions.items():
            current_price = current_prices.get(symbol, 0)
            if current_price > 0:
                position_value = position['quantity'] * current_price
                position_pnl = (current_price - position['entry_price']) * position['quantity']
                
                total_value += position_value
                unrealized_pnl += position_pnl
        
        total_pnl = total_value - self.initial_capital
        total_pnl_percent = (total_pnl / self.initial_capital * 100) if self.initial_capital > 0 else 0
        
        return {
            'initial_capital': self.initial_capital,
            'current_value': total_value,
            'total_pnl': total_pnl,
            'total_pnl_percent': total_pnl_percent,
            'unrealized_pnl': unrealized_pnl,
            'num_positions': len(self.positions),
            'symbols_monitored': len(self.symbols)
        }
    
    def get_portfolio_summary(self, current_prices: Dict[str, float]) -> List[Dict]:
        """
        Retorna resumo detalhado do portfolio
        
        Returns:
            Lista com info de cada símbolo
        """
        summary = []
        
        for symbol in self.symbols:
            current_price = current_prices.get(symbol, 0)
            
            if symbol in self.positions:
                # Em posição
                position = self.positions[symbol]
                pnl = (current_price - position['entry_price']) * position['quantity']
                pnl_percent = ((current_price - position['entry_price']) / position['entry_price']) * 100
                
                summary.append({
                    'symbol': symbol,
                    'status': 'open',
                    'entry_price': position['entry_price'],
                    'current_price': current_price,
                    'quantity': position['quantity'],
                    'pnl': pnl,
                    'pnl_percent': pnl_percent,
                    'stop_loss': position['stop_loss'],
                    'take_profit': position['take_profit']
                })
            else:
                # Sem posição
                summary.append({
                    'symbol': symbol,
                    'status': 'monitoring',
                    'current_price': current_price,
                    'allocated_capital': self.capital_allocation.get(symbol, 0)
                })
        
        return summary







