"""
Sistema de Gerenciamento de Risco
Controla tamanho de posição, stop loss, take profit e limites
"""

import logging
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta
from config.settings import Settings

logger = logging.getLogger(__name__)


class RiskManager:
    """
    Gerenciador de risco para trading
    - Calcula tamanho de posição
    - Define stop loss e take profit
    - Controla drawdown
    - Limita número de trades
    """
    
    def __init__(self, exchange=None, data_manager=None):
        """
        Inicializa o gerenciador de risco
        
        Args:
            exchange: Instância do BinanceExchange
            data_manager: Instância do DataManager
        """
        self.settings = Settings()
        self.exchange = exchange
        self.data_manager = data_manager
        
        # Estado interno
        self.initial_balance = 0.0
        self.peak_balance = 0.0
        self.trades_today = 0
        self.last_trade_date = None
        self.is_paused = False
        self.pause_reason = ""
    
    def initialize(self):
        """Inicializa o gerenciador (deve ser chamado após conexão com exchange)"""
        if self.exchange:
            self.initial_balance = self.exchange.get_usdt_balance()
            self.peak_balance = self.initial_balance
            logger.info(f"💰 Saldo inicial: ${self.initial_balance:.2f} USDT")
    
    def update_balance(self):
        """Atualiza o saldo e verifica drawdown"""
        if not self.exchange:
            return
        
        current_balance = self.exchange.get_usdt_balance()
        
        # Atualizar pico
        if current_balance > self.peak_balance:
            self.peak_balance = current_balance
        
        # Verificar drawdown
        if self.peak_balance > 0:
            drawdown = (self.peak_balance - current_balance) / self.peak_balance
            
            if drawdown >= self.settings.MAX_DRAWDOWN_PERCENT:
                self.pause(f"Drawdown de {drawdown*100:.2f}% atingido (limite: {self.settings.MAX_DRAWDOWN_PERCENT*100:.2f}%)")
                logger.error(f"🚨 BOT PAUSADO: Drawdown máximo atingido!")
    
    def reset_daily_counter(self):
        """Reseta o contador de trades diários"""
        today = datetime.now().date()
        
        if self.last_trade_date != today:
            self.trades_today = 0
            self.last_trade_date = today
            logger.info(f"🔄 Contador de trades resetado para {today}")
    
    def can_trade(self) -> Tuple[bool, str]:
        """
        Verifica se pode executar um novo trade
        
        Returns:
            (pode_tradear, motivo)
        """
        # Bot pausado?
        if self.is_paused:
            return False, f"Bot pausado: {self.pause_reason}"
        
        # Atualizar contador diário
        self.reset_daily_counter()
        
        # Verificar limite de trades por dia
        if self.trades_today >= self.settings.MAX_TRADES_PER_DAY:
            return False, f"Limite diário de trades atingido ({self.settings.MAX_TRADES_PER_DAY})"
        
        # Verificar saldo disponível
        if self.exchange:
            balance = self.exchange.get_usdt_balance()
            min_balance = 2.0  # Mínimo de $2 USDT (R$ 10)
            
            if balance < min_balance:
                return False, f"Saldo insuficiente: ${balance:.2f} USDT (mínimo: ${min_balance})"
        
        return True, "OK"
    
    def calculate_position_size(self, symbol: str = None) -> Dict:
        """
        Calcula o tamanho da posição baseado no risco
        
        Args:
            symbol: Par de trading
        
        Returns:
            {
                'usdt_amount': valor em USDT,
                'quantity': quantidade da moeda,
                'percentage': percentual do saldo usado
            }
        """
        symbol = symbol or self.settings.TRADING_SYMBOL
        
        if not self.exchange:
            logger.error("Exchange não configurada")
            return {'usdt_amount': 0, 'quantity': 0, 'percentage': 0}
        
        try:
            # Obter saldo disponível
            balance = self.exchange.get_usdt_balance()
            
            # Calcular valor da posição
            usdt_amount = balance * self.settings.POSITION_SIZE_PERCENT
            
            # Calcular quantidade
            quantity = self.exchange.calculate_quantity(symbol, usdt_amount)
            
            logger.info(f"📊 Posição calculada: ${usdt_amount:.2f} USDT = {quantity} {symbol}")
            
            return {
                'usdt_amount': usdt_amount,
                'quantity': quantity,
                'percentage': self.settings.POSITION_SIZE_PERCENT * 100,
                'current_balance': balance
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao calcular posição: {e}")
            return {'usdt_amount': 0, 'quantity': 0, 'percentage': 0}
    
    def calculate_stop_loss(self, entry_price: float, side: str = 'buy') -> float:
        """
        Calcula o preço de stop loss
        
        Args:
            entry_price: Preço de entrada
            side: 'buy' ou 'sell'
        
        Returns:
            Preço de stop loss
        """
        if side == 'buy':
            # Para compra, stop loss abaixo do preço
            stop_price = entry_price * (1 - self.settings.STOP_LOSS_PERCENT)
        else:
            # Para venda, stop loss acima do preço
            stop_price = entry_price * (1 + self.settings.STOP_LOSS_PERCENT)
        
        logger.debug(f"🛑 Stop Loss: ${stop_price:.2f} ({self.settings.STOP_LOSS_PERCENT*100:.2f}%)")
        return stop_price
    
    def calculate_take_profit(self, entry_price: float, side: str = 'buy') -> float:
        """
        Calcula o preço de take profit
        
        Args:
            entry_price: Preço de entrada
            side: 'buy' ou 'sell'
        
        Returns:
            Preço de take profit
        """
        if side == 'buy':
            # Para compra, take profit acima do preço
            tp_price = entry_price * (1 + self.settings.TAKE_PROFIT_PERCENT)
        else:
            # Para venda, take profit abaixo do preço
            tp_price = entry_price * (1 - self.settings.TAKE_PROFIT_PERCENT)
        
        logger.debug(f"🎯 Take Profit: ${tp_price:.2f} ({self.settings.TAKE_PROFIT_PERCENT*100:.2f}%)")
        return tp_price
    
    def calculate_trailing_stop(self, entry_price: float, current_price: float, 
                                highest_price: float, side: str = 'buy') -> Optional[float]:
        """
        Calcula trailing stop loss (stop que acompanha o lucro)
        
        Args:
            entry_price: Preço de entrada
            current_price: Preço atual
            highest_price: Maior preço desde a entrada
            side: 'buy' ou 'sell'
        
        Returns:
            Novo preço de stop ou None se não houver mudança
        """
        if not self.settings.USE_TRAILING_STOP:
            return None
        
        if side == 'buy':
            # Apenas ativar trailing stop se estiver em lucro
            if current_price <= entry_price:
                return None
            
            # Calcular stop baseado no pico
            trailing_stop = highest_price * (1 - self.settings.TRAILING_STOP_PERCENT)
            
            # Stop nunca deve ir abaixo do break-even
            if trailing_stop < entry_price:
                trailing_stop = entry_price
            
            return trailing_stop
        else:
            # Para vendas (short)
            if current_price >= entry_price:
                return None
            
            lowest_price = highest_price  # Usar como menor preço
            trailing_stop = lowest_price * (1 + self.settings.TRAILING_STOP_PERCENT)
            
            if trailing_stop > entry_price:
                trailing_stop = entry_price
            
            return trailing_stop
    
    def should_exit(self, entry_price: float, current_price: float, 
                   stop_loss: float, take_profit: float, side: str = 'buy') -> Tuple[bool, str]:
        """
        Verifica se deve sair da posição
        
        Args:
            entry_price: Preço de entrada
            current_price: Preço atual
            stop_loss: Preço de stop loss
            take_profit: Preço de take profit
            side: 'buy' ou 'sell'
        
        Returns:
            (deve_sair, motivo)
        """
        if side == 'buy':
            # Stop Loss atingido
            if current_price <= stop_loss:
                return True, f"Stop Loss (${stop_loss:.2f})"
            
            # Take Profit atingido
            if current_price >= take_profit:
                return True, f"Take Profit (${take_profit:.2f})"
        
        else:  # sell/short
            # Stop Loss atingido
            if current_price >= stop_loss:
                return True, f"Stop Loss (${stop_loss:.2f})"
            
            # Take Profit atingido
            if current_price <= take_profit:
                return True, f"Take Profit (${take_profit:.2f})"
        
        return False, ""
    
    def record_trade(self):
        """Registra um trade executado"""
        self.trades_today += 1
        logger.info(f"📈 Trade #{self.trades_today} registrado hoje")
    
    def pause(self, reason: str):
        """Pausa o bot"""
        self.is_paused = True
        self.pause_reason = reason
        logger.warning(f"⏸️  Bot pausado: {reason}")
    
    def resume(self):
        """Resume o bot"""
        self.is_paused = False
        self.pause_reason = ""
        logger.info("▶️  Bot resumido")
    
    def get_risk_summary(self) -> Dict:
        """Retorna resumo do gerenciamento de risco"""
        current_balance = self.exchange.get_usdt_balance() if self.exchange else 0
        
        profit_loss = current_balance - self.initial_balance
        profit_loss_percent = (profit_loss / self.initial_balance * 100) if self.initial_balance > 0 else 0
        
        current_drawdown = 0
        if self.peak_balance > 0:
            current_drawdown = (self.peak_balance - current_balance) / self.peak_balance * 100
        
        return {
            'initial_balance': self.initial_balance,
            'current_balance': current_balance,
            'peak_balance': self.peak_balance,
            'profit_loss': profit_loss,
            'profit_loss_percent': profit_loss_percent,
            'current_drawdown': current_drawdown,
            'max_drawdown_limit': self.settings.MAX_DRAWDOWN_PERCENT * 100,
            'trades_today': self.trades_today,
            'max_trades_per_day': self.settings.MAX_TRADES_PER_DAY,
            'is_paused': self.is_paused,
            'pause_reason': self.pause_reason,
        }
    
    def validate_order(self, order_type: str, symbol: str, quantity: float, 
                      price: float = None) -> Tuple[bool, str]:
        """
        Valida uma ordem antes de executar
        
        Args:
            order_type: 'buy' ou 'sell'
            symbol: Par de trading
            quantity: Quantidade
            price: Preço (para ordens limitadas)
        
        Returns:
            (válido, mensagem)
        """
        # Verificar se pode tradear
        can_trade, reason = self.can_trade()
        if not can_trade:
            return False, reason
        
        # Verificar quantidade mínima
        if quantity <= 0:
            return False, "Quantidade inválida"
        
        # Verificar saldo
        if self.exchange:
            if order_type == 'buy':
                balance = self.exchange.get_usdt_balance()
                required = quantity * (price or self.exchange.get_current_price(symbol))
                
                if required > balance:
                    return False, f"Saldo insuficiente: precisa ${required:.2f}, tem ${balance:.2f}"
        
        return True, "Ordem válida"

