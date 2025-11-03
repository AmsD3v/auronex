"""
Sistema de conexão Multi-Exchange
Suporta Binance, Bybit, e futuras corretoras
"""

import ccxt
import logging
from typing import Optional, Dict
import pandas as pd
from config.settings import Settings

logger = logging.getLogger(__name__)


class MultiExchange:
    """
    Classe para conectar com múltiplas corretoras
    Atualmente suporta: Binance, Bybit
    """
    
    def __init__(self, exchange_name: str = "Binance"):
        """
        Inicializa conexão com corretora escolhida
        
        Args:
            exchange_name: "Binance", "Bybit", "OKX", etc
        """
        self.settings = Settings()
        self.exchange_name = exchange_name
        self.exchange = None
        self.connect()
    
    def connect(self):
        """Estabelece conexão com a corretora selecionada"""
        try:
            if self.exchange_name == "Binance":
                self._connect_binance()
            elif self.exchange_name == "Bybit":
                self._connect_bybit()
            else:
                logger.error(f"Corretora {self.exchange_name} não implementada ainda")
                return False
            
            # Testar conexão
            self.exchange.load_markets()
            logger.info(f"Conectado com sucesso a {self.exchange_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao conectar com {self.exchange_name}: {e}")
            raise
    
    def _connect_binance(self):
        """Conecta à Binance"""
        logger.info(f"Conectando à Binance ({self.get_mode()})...")
        
        self.exchange = ccxt.binance({
            'apiKey': self.settings.BINANCE_API_KEY,
            'secret': self.settings.BINANCE_SECRET_KEY,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,
                'recvWindow': 60000,  # 60 segundos de janela para evitar erros de timestamp
            }
        })
        
        if self.settings.USE_TESTNET:
            self.exchange.set_sandbox_mode(True)
        
        # Sincronizar timestamp com servidor Binance
        try:
            self.exchange.load_time_difference()
            logger.info("Timestamp sincronizado com servidor Binance")
        except Exception as e:
            logger.warning(f"Aviso ao sincronizar timestamp: {e}")
    
    def _connect_bybit(self):
        """Conecta à Bybit"""
        logger.info(f"Conectando à Bybit ({self.get_mode()})...")
        
        self.exchange = ccxt.bybit({
            'apiKey': self.settings.BYBIT_API_KEY,
            'secret': self.settings.BYBIT_SECRET_KEY,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
                'recvWindow': 60000,  # 60 segundos de janela
            }
        })
        
        if self.settings.USE_TESTNET:
            self.exchange.set_sandbox_mode(True)
        
        # Sincronizar timestamp com servidor
        try:
            self.exchange.load_time_difference()
        except:
            pass
    
    def get_mode(self) -> str:
        """Retorna modo de operação"""
        return "TESTNET" if self.settings.USE_TESTNET else "PRODUÇÃO"
    
    def get_ticker(self, symbol: str) -> Optional[Dict]:
        """Obtém ticker de um símbolo"""
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            logger.error(f"Erro ao obter ticker de {symbol}: {e}")
            return None
    
    def get_ohlcv(self, symbol: str, timeframe: str = None, limit: int = 100) -> pd.DataFrame:
        """Obtém dados OHLCV"""
        timeframe = timeframe or self.settings.TIMEFRAME
        
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"Erro ao obter OHLCV de {symbol}: {e}")
            return pd.DataFrame()
    
    def create_market_order(self, symbol: str, side: str, amount: float) -> Optional[Dict]:
        """Cria ordem a mercado"""
        try:
            if self.settings.PAPER_TRADING:
                logger.info(f"[PAPER] Ordem {side.upper()} de {amount} {symbol}")
                return {
                    'id': f'paper_{pd.Timestamp.now().timestamp()}',
                    'symbol': symbol,
                    'side': side,
                    'amount': amount,
                    'status': 'closed',
                    'paper_trading': True
                }
            
            order = self.exchange.create_market_order(symbol, side, amount)
            logger.info(f"Ordem {side.upper()} executada: {amount} {symbol}")
            return order
            
        except Exception as e:
            logger.error(f"Erro ao criar ordem: {e}")
            return None
    
    def get_balance(self) -> Dict:
        """Obtém saldo da conta"""
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            logger.error(f"Erro ao obter saldo: {e}")
            return {}
    
    def get_usdt_balance(self) -> float:
        """Retorna saldo USDT"""
        try:
            balance = self.get_balance()
            return balance.get('USDT', {}).get('free', 0.0)
        except:
            return 0.0
    
    def calculate_quantity(self, symbol: str, usdt_amount: float) -> float:
        """Calcula quantidade baseado em valor USDT"""
        try:
            ticker = self.get_ticker(symbol)
            if ticker and ticker['last'] > 0:
                return usdt_amount / ticker['last']
            return 0.0
        except:
            return 0.0

