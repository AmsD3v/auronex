"""
Sistema de coleta e armazenamento de dados
Gerencia dados históricos e em tempo real
"""

import logging
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from config.settings import Settings

logger = logging.getLogger(__name__)


class DataManager:
    """
    Gerenciador de dados de trading
    - Coleta dados históricos
    - Armazena em banco de dados SQLite
    - Fornece dados para estratégias e backtesting
    """
    
    def __init__(self, exchange=None):
        """
        Inicializa o gerenciador de dados
        
        Args:
            exchange: Instância do BinanceExchange
        """
        self.settings = Settings()
        self.exchange = exchange
        self.db_path = self.settings.DATA_DIR / 'trading.db'
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabela para dados OHLCV
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ohlcv (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    timeframe TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume REAL NOT NULL,
                    UNIQUE(symbol, timeframe, timestamp)
                )
            ''')
            
            # Tabela para ordens executadas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    price REAL,
                    cost REAL,
                    fee REAL,
                    status TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    strategy TEXT,
                    paper_trading BOOLEAN DEFAULT 0,
                    UNIQUE(order_id)
                )
            ''')
            
            # Tabela para trades (pares de compra/venda)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    entry_order_id TEXT NOT NULL,
                    exit_order_id TEXT,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    quantity REAL NOT NULL,
                    entry_time INTEGER NOT NULL,
                    exit_time INTEGER,
                    profit_loss REAL,
                    profit_loss_percent REAL,
                    strategy TEXT,
                    status TEXT DEFAULT 'open',
                    paper_trading BOOLEAN DEFAULT 0
                )
            ''')
            
            # Tabela para performance diária
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    initial_balance REAL NOT NULL,
                    final_balance REAL NOT NULL,
                    profit_loss REAL NOT NULL,
                    profit_loss_percent REAL NOT NULL,
                    num_trades INTEGER DEFAULT 0,
                    winning_trades INTEGER DEFAULT 0,
                    losing_trades INTEGER DEFAULT 0,
                    UNIQUE(date)
                )
            ''')
            
            # Índices para melhorar performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_ohlcv_symbol_timeframe 
                ON ohlcv(symbol, timeframe, timestamp DESC)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_orders_timestamp 
                ON orders(timestamp DESC)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_trades_status 
                ON trades(status, entry_time DESC)
            ''')
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Banco de dados inicializado: {self.db_path}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar banco de dados: {e}")
            raise
    
    def save_ohlcv(self, df: pd.DataFrame, symbol: str = None, timeframe: str = None):
        """
        Salva dados OHLCV no banco de dados
        
        Args:
            df: DataFrame com colunas: timestamp, open, high, low, close, volume
            symbol: Par de trading
            timeframe: Período
        """
        symbol = symbol or self.settings.TRADING_SYMBOL
        timeframe = timeframe or self.settings.TIMEFRAME
        
        if df.empty:
            logger.warning("DataFrame vazio, nada para salvar")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Preparar dados
            df_to_save = df.copy()
            df_to_save['symbol'] = symbol
            df_to_save['timeframe'] = timeframe
            
            # Converter timestamp para unix timestamp (inteiro)
            if df_to_save.index.name == 'timestamp':
                df_to_save['timestamp'] = (df_to_save.index.astype('int64') // 10**9).astype(int)
            
            # Reordenar colunas
            columns = ['symbol', 'timeframe', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
            df_to_save = df_to_save[columns]
            
            # Salvar (ignorar duplicatas)
            df_to_save.to_sql('ohlcv', conn, if_exists='append', index=False)
            
            conn.commit()
            conn.close()
            logger.debug(f"✅ {len(df_to_save)} candles salvos para {symbol} ({timeframe})")
            
        except sqlite3.IntegrityError:
            # Duplicatas ignoradas
            pass
        except Exception as e:
            logger.error(f"❌ Erro ao salvar OHLCV: {e}")
    
    def load_ohlcv(self, symbol: str = None, timeframe: str = None, 
                   limit: int = None, start_date: datetime = None) -> pd.DataFrame:
        """
        Carrega dados OHLCV do banco de dados
        
        Args:
            symbol: Par de trading
            timeframe: Período
            limit: Número máximo de candles
            start_date: Data inicial
        
        Returns:
            DataFrame com dados OHLCV
        """
        symbol = symbol or self.settings.TRADING_SYMBOL
        timeframe = timeframe or self.settings.TIMEFRAME
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = f'''
                SELECT timestamp, open, high, low, close, volume
                FROM ohlcv
                WHERE symbol = ? AND timeframe = ?
            '''
            
            params = [symbol, timeframe]
            
            if start_date:
                start_timestamp = int(start_date.timestamp())
                query += ' AND timestamp >= ?'
                params.append(start_timestamp)
            
            query += ' ORDER BY timestamp ASC'
            
            if limit:
                query += f' LIMIT {limit}'
            
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            
            if not df.empty:
                # Converter timestamp para datetime
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar OHLCV: {e}")
            return pd.DataFrame()
    
    def download_historical_data(self, symbol: str = None, timeframe: str = None, 
                                days: int = 30) -> pd.DataFrame:
        """
        Baixa dados históricos da exchange e salva no banco
        
        Args:
            symbol: Par de trading
            timeframe: Período
            days: Número de dias de histórico
        
        Returns:
            DataFrame com dados baixados
        """
        if not self.exchange:
            logger.error("Exchange não configurada")
            return pd.DataFrame()
        
        symbol = symbol or self.settings.TRADING_SYMBOL
        timeframe = timeframe or self.settings.TIMEFRAME
        
        try:
            # Calcular quantos candles precisamos
            minutes_per_candle = self.settings.get_timeframe_minutes(timeframe)
            total_candles = (days * 24 * 60) // minutes_per_candle
            
            # Limitar a 1000 candles por requisição (limite da Binance)
            batch_size = 1000
            all_data = []
            
            logger.info(f"📥 Baixando {total_candles} candles de {symbol} ({timeframe})...")
            
            for i in range(0, total_candles, batch_size):
                remaining = min(batch_size, total_candles - i)
                df_batch = self.exchange.get_ohlcv(symbol, timeframe, limit=remaining)
                
                if not df_batch.empty:
                    all_data.append(df_batch)
                    # Salvar no banco
                    if self.settings.SAVE_HISTORICAL_DATA:
                        self.save_ohlcv(df_batch, symbol, timeframe)
            
            if all_data:
                df_complete = pd.concat(all_data).drop_duplicates()
                logger.info(f"✅ {len(df_complete)} candles baixados e salvos")
                return df_complete
            
            return pd.DataFrame()
            
        except Exception as e:
            logger.error(f"❌ Erro ao baixar dados históricos: {e}")
            return pd.DataFrame()
    
    def save_order(self, order: dict):
        """Salva uma ordem no banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO orders 
                (order_id, symbol, side, type, amount, price, cost, fee, status, timestamp, paper_trading)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                order.get('id'),
                order.get('symbol'),
                order.get('side'),
                order.get('type', 'market'),
                order.get('amount', 0),
                order.get('price', 0),
                order.get('cost', 0),
                order.get('fee', {}).get('cost', 0),
                order.get('status'),
                int(datetime.now().timestamp()),
                order.get('paper_trading', False)
            ))
            
            conn.commit()
            conn.close()
            logger.debug(f"✅ Ordem {order.get('id')} salva no banco")
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar ordem: {e}")
    
    def get_orders_history(self, limit: int = 100) -> List[dict]:
        """Retorna histórico de ordens"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM orders
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            columns = [col[0] for col in cursor.description]
            orders = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return orders
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter histórico de ordens: {e}")
            return []
    
    def get_open_trades(self) -> List[dict]:
        """Retorna trades abertos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM trades
                WHERE status = 'open'
                ORDER BY entry_time DESC
            ''')
            
            columns = [col[0] for col in cursor.description]
            trades = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            conn.close()
            return trades
            
        except Exception as e:
            logger.error(f"❌ Erro ao obter trades abertos: {e}")
            return []
    
    def get_performance_summary(self, days: int = 7) -> dict:
        """
        Retorna resumo de performance
        
        Args:
            days: Número de dias para análise
        
        Returns:
            Dicionário com métricas de performance
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            since_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())
            
            # Total de trades
            cursor.execute('''
                SELECT COUNT(*) FROM trades
                WHERE entry_time >= ? AND status = 'closed'
            ''', (since_timestamp,))
            total_trades = cursor.fetchone()[0]
            
            # Trades vencedores
            cursor.execute('''
                SELECT COUNT(*) FROM trades
                WHERE entry_time >= ? AND status = 'closed' AND profit_loss > 0
            ''', (since_timestamp,))
            winning_trades = cursor.fetchone()[0]
            
            # Profit/Loss total
            cursor.execute('''
                SELECT SUM(profit_loss) FROM trades
                WHERE entry_time >= ? AND status = 'closed'
            ''', (since_timestamp,))
            total_pl = cursor.fetchone()[0] or 0
            
            conn.close()
            
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            return {
                'period_days': days,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'losing_trades': total_trades - winning_trades,
                'win_rate': win_rate,
                'total_profit_loss': total_pl,
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao calcular performance: {e}")
            return {}

