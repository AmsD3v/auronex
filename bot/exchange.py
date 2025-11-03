"""
Sistema de conexão com a Binance
Suporta Testnet e Produção
"""

import ccxt
import logging
from typing import Optional, Dict, List, Any
from datetime import datetime
import pandas as pd
from config.settings import Settings

logger = logging.getLogger(__name__)


class BinanceExchange:
    """
    Classe para interagir com a Binance
    Suporta Testnet e Produção
    """
    
    def __init__(self):
        """Inicializa a conexão com a Binance"""
        self.settings = Settings()
        self.exchange = None
        self.connect()
    
    def connect(self):
        """Estabelece conexão com a Binance"""
        try:
            if self.settings.USE_TESTNET:
                logger.info("🧪 Conectando ao Binance TESTNET...")
                self.exchange = ccxt.binance({
                    'apiKey': self.settings.BINANCE_API_KEY,
                    'secret': self.settings.BINANCE_SECRET_KEY,
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'spot',
                        'adjustForTimeDifference': True,
                    }
                })
                # Configurar para testnet
                self.exchange.set_sandbox_mode(True)
            else:
                logger.info("⚠️  Conectando ao Binance PRODUÇÃO...")
                self.exchange = ccxt.binance({
                    'apiKey': self.settings.BINANCE_API_KEY,
                    'secret': self.settings.BINANCE_SECRET_KEY,
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'spot',
                        'adjustForTimeDifference': True,
                    }
                })
            
            # Testar conexão
            self.exchange.load_markets()
            logger.info(f"✅ Conectado com sucesso à Binance ({self.get_mode()})")
            
        except Exception as e:
            logger.error(f"❌ Erro ao conectar com Binance: {e}")
            raise
    
    def get_mode(self) -> str:
        """Retorna o modo de operação"""
        return "TESTNET" if self.settings.USE_TESTNET else "PRODUÇÃO"
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Testa a conexão com a Binance
        Retorna (sucesso, mensagem)
        """
        try:
            # Testar se consegue buscar o ticker
            ticker = self.exchange.fetch_ticker(self.settings.TRADING_SYMBOL)
            balance = self.get_balance()
            
            msg = f"""
✅ Conexão OK!
Modo: {self.get_mode()}
Símbolo: {self.settings.TRADING_SYMBOL}
Preço Atual: ${ticker['last']:.2f}
Saldo USDT: ${balance['USDT']['free']:.2f}
            """
            return True, msg
            
        except Exception as e:
            return False, f"❌ Erro na conexão: {str(e)}"
    
    def get_balance(self) -> Dict[str, Dict[str, float]]:
        """
        Obtém o saldo da conta
        Retorna: {'BTC': {'free': 0.1, 'used': 0.0, 'total': 0.1}, ...}
        """
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            logger.error(f"Erro ao obter saldo: {e}")
            return {}
    
    def get_usdt_balance(self) -> float:
        """Retorna apenas o saldo disponível em USDT"""
        try:
            balance = self.get_balance()
            return balance.get('USDT', {}).get('free', 0.0)
        except Exception as e:
            logger.error(f"Erro ao obter saldo USDT: {e}")
            return 0.0
    
    def get_ticker(self, symbol: str = None) -> Optional[Dict]:
        """
        Obtém informações de preço de um símbolo
        """
        symbol = symbol or self.settings.TRADING_SYMBOL
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"Erro ao obter ticker de {symbol}: {e}")
            return None
    
    def get_current_price(self, symbol: str = None) -> float:
        """Retorna o preço atual de um símbolo"""
        ticker = self.get_ticker(symbol)
        if ticker:
            return ticker['last']
        return 0.0
    
    def get_ohlcv(self, symbol: str = None, timeframe: str = None, 
                   limit: int = 100) -> pd.DataFrame:
        """
        Obtém dados OHLCV (Open, High, Low, Close, Volume)
        
        Args:
            symbol: Par de trading (ex: 'BTCUSDT')
            timeframe: Período (ex: '1m', '5m', '1h')
            limit: Número de candles
        
        Returns:
            DataFrame com colunas: timestamp, open, high, low, close, volume
        """
        symbol = symbol or self.settings.TRADING_SYMBOL
        timeframe = timeframe or self.settings.TIMEFRAME
        
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # Converter timestamp para datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao obter OHLCV de {symbol}: {e}")
            return pd.DataFrame()
    
    def create_market_order(self, symbol: str, side: str, amount: float) -> Optional[Dict]:
        """
        Cria uma ordem a mercado
        
        Args:
            symbol: Par de trading
            side: 'buy' ou 'sell'
            amount: Quantidade em moeda base
        
        Returns:
            Informações da ordem criada
        """
        try:
            if self.settings.PAPER_TRADING:
                logger.info(f"📝 [PAPER] Ordem {side.upper()} de {amount} {symbol}")
                return {
                    'id': f'paper_{datetime.now().timestamp()}',
                    'symbol': symbol,
                    'side': side,
                    'amount': amount,
                    'status': 'closed',
                    'paper_trading': True
                }
            
            order = self.exchange.create_market_order(symbol, side, amount)
            logger.info(f"✅ Ordem {side.upper()} executada: {amount} {symbol}")
            return order
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar ordem: {e}")
            return None
    
    def create_limit_order(self, symbol: str, side: str, amount: float, 
                          price: float) -> Optional[Dict]:
        """
        Cria uma ordem limitada
        
        Args:
            symbol: Par de trading
            side: 'buy' ou 'sell'
            amount: Quantidade
            price: Preço limite
        
        Returns:
            Informações da ordem criada
        """
        try:
            if self.settings.PAPER_TRADING:
                logger.info(f"📝 [PAPER] Ordem LIMIT {side.upper()} de {amount} {symbol} @ ${price}")
                return {
                    'id': f'paper_{datetime.now().timestamp()}',
                    'symbol': symbol,
                    'side': side,
                    'amount': amount,
                    'price': price,
                    'status': 'open',
                    'paper_trading': True
                }
            
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            logger.info(f"✅ Ordem LIMIT {side.upper()} criada: {amount} {symbol} @ ${price}")
            return order
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar ordem limitada: {e}")
            return None
    
    def cancel_order(self, order_id: str, symbol: str = None) -> bool:
        """Cancela uma ordem"""
        symbol = symbol or self.settings.TRADING_SYMBOL
        
        try:
            if self.settings.PAPER_TRADING:
                logger.info(f"📝 [PAPER] Ordem {order_id} cancelada")
                return True
            
            self.exchange.cancel_order(order_id, symbol)
            logger.info(f"✅ Ordem {order_id} cancelada")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao cancelar ordem: {e}")
            return False
    
    def get_open_orders(self, symbol: str = None) -> List[Dict]:
        """Retorna todas as ordens abertas"""
        symbol = symbol or self.settings.TRADING_SYMBOL
        
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            return orders
        except Exception as e:
            logger.error(f"Erro ao obter ordens abertas: {e}")
            return []
    
    def get_order(self, order_id: str, symbol: str = None) -> Optional[Dict]:
        """Obtém informações de uma ordem específica"""
        symbol = symbol or self.settings.TRADING_SYMBOL
        
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return order
        except Exception as e:
            logger.error(f"Erro ao obter ordem {order_id}: {e}")
            return None
    
    def get_symbol_info(self, symbol: str = None) -> Optional[Dict]:
        """Obtém informações sobre um símbolo (limites, precisão, etc)"""
        symbol = symbol or self.settings.TRADING_SYMBOL
        
        try:
            markets = self.exchange.load_markets()
            return markets.get(symbol, None)
        except Exception as e:
            logger.error(f"Erro ao obter info do símbolo {symbol}: {e}")
            return None
    
    def calculate_quantity(self, symbol: str, usdt_amount: float) -> float:
        """
        Calcula a quantidade de moeda baseado no valor em USDT
        
        Args:
            symbol: Par de trading
            usdt_amount: Valor em USDT
        
        Returns:
            Quantidade da moeda base
        """
        try:
            price = self.get_current_price(symbol)
            if price > 0:
                quantity = usdt_amount / price
                
                # Arredondar para a precisão correta
                symbol_info = self.get_symbol_info(symbol)
                if symbol_info:
                    precision = symbol_info['precision']['amount']
                    quantity = round(quantity, precision)
                
                return quantity
            return 0.0
        except Exception as e:
            logger.error(f"Erro ao calcular quantidade: {e}")
            return 0.0

