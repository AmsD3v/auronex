"""
Configurações do RoboTrader
Carrega variáveis de ambiente e define configurações padrão
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

# Carregar override local primeiro (se existir)
try:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    import env_local_override
except ImportError:
    pass

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Settings:
    """Classe centralizada de configurações"""
    
    # ========================================
    # PATHS
    # ========================================
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / 'data'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Criar diretórios se não existirem
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # ========================================
    # BINANCE API
    # ========================================
    USE_TESTNET = os.getenv('USE_TESTNET', 'True').lower() == 'true'
    
    if USE_TESTNET:
        BINANCE_API_KEY = os.getenv('BINANCE_TESTNET_API_KEY', '')
        BINANCE_SECRET_KEY = os.getenv('BINANCE_TESTNET_SECRET_KEY', '')
        BINANCE_BASE_URL = 'https://testnet.binance.vision/api'
    else:
        BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
        BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY', '')
        BINANCE_BASE_URL = 'https://api.binance.com/api'
    
    # ========================================
    # BYBIT API
    # ========================================
    if USE_TESTNET:
        BYBIT_API_KEY = os.getenv('BYBIT_TESTNET_API_KEY', '')
        BYBIT_SECRET_KEY = os.getenv('BYBIT_TESTNET_SECRET_KEY', '')
    else:
        BYBIT_API_KEY = os.getenv('BYBIT_API_KEY', '')
        BYBIT_SECRET_KEY = os.getenv('BYBIT_SECRET_KEY', '')
    
    # ========================================
    # TRADING
    # ========================================
    TRADING_SYMBOL = os.getenv('TRADING_SYMBOL', 'BTCUSDT')
    TIMEFRAME = os.getenv('TIMEFRAME', '15m')
    STRATEGY = os.getenv('STRATEGY', 'trend_following')
    
    # ========================================
    # GERENCIAMENTO DE RISCO
    # ========================================
    POSITION_SIZE_PERCENT = float(os.getenv('POSITION_SIZE_PERCENT', '0.10'))  # 10% do saldo
    STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT', '0.02'))  # 2% de perda
    TAKE_PROFIT_PERCENT = float(os.getenv('TAKE_PROFIT_PERCENT', '0.04'))  # 4% de lucro
    MAX_DRAWDOWN_PERCENT = float(os.getenv('MAX_DRAWDOWN_PERCENT', '0.10'))  # 10% drawdown máximo
    MAX_TRADES_PER_DAY = int(os.getenv('MAX_TRADES_PER_DAY', '10'))
    
    # Trailing Stop
    USE_TRAILING_STOP = True
    TRAILING_STOP_PERCENT = 0.015  # 1.5%
    
    # ========================================
    # TELEGRAM
    # ========================================
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    ENABLE_TELEGRAM = os.getenv('ENABLE_TELEGRAM', 'False').lower() == 'true'
    
    # ========================================
    # SISTEMA
    # ========================================
    UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', '60'))  # segundos
    SAVE_HISTORICAL_DATA = os.getenv('SAVE_HISTORICAL_DATA', 'True').lower() == 'true'
    DEBUG_MODE = os.getenv('DEBUG_MODE', 'True').lower() == 'true'
    PAPER_TRADING = os.getenv('PAPER_TRADING', 'True').lower() == 'true'
    
    # ========================================
    # BANCO DE DADOS
    # ========================================
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DATA_DIR}/trading.db')
    
    # ========================================
    # INDICADORES TÉCNICOS - TREND FOLLOWING
    # ========================================
    EMA_FAST = 9
    EMA_MEDIUM = 21
    EMA_SLOW = 50
    RSI_PERIOD = 14
    RSI_OVERBOUGHT = 70
    RSI_OVERSOLD = 30
    
    # ========================================
    # INDICADORES TÉCNICOS - MEAN REVERSION
    # ========================================
    BOLLINGER_PERIOD = 20
    BOLLINGER_STD = 2
    
    # ========================================
    # BACKTESTING
    # ========================================
    BACKTEST_INITIAL_CAPITAL = 10000  # USDT
    BACKTEST_COMMISSION = 0.001  # 0.1%
    
    # ========================================
    # TIMEFRAME CONVERSION
    # ========================================
    TIMEFRAME_TO_MINUTES: Dict[str, int] = {
        '1m': 1,
        '3m': 3,
        '5m': 5,
        '15m': 15,
        '30m': 30,
        '1h': 60,
        '2h': 120,
        '4h': 240,
        '6h': 360,
        '12h': 720,
        '1d': 1440,
        '3d': 4320,
        '1w': 10080,
    }
    
    @classmethod
    def get_timeframe_minutes(cls, timeframe: str = None) -> int:
        """Retorna o timeframe em minutos"""
        tf = timeframe or cls.TIMEFRAME
        return cls.TIMEFRAME_TO_MINUTES.get(tf, 15)
    
    @classmethod
    def validate_config(cls) -> tuple[bool, str]:
        """
        Valida se as configurações estão corretas
        Retorna (válido, mensagem_erro)
        """
        if not cls.BINANCE_API_KEY:
            return False, "API Key da Binance não configurada"
        
        if not cls.BINANCE_SECRET_KEY:
            return False, "Secret Key da Binance não configurada"
        
        if cls.TRADING_SYMBOL not in ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'DOGEUSDT', 'SOLUSDT']:
            return False, f"Símbolo {cls.TRADING_SYMBOL} pode não ser válido. Use pares com USDT"
        
        if cls.TIMEFRAME not in cls.TIMEFRAME_TO_MINUTES:
            return False, f"Timeframe {cls.TIMEFRAME} inválido"
        
        if cls.POSITION_SIZE_PERCENT <= 0 or cls.POSITION_SIZE_PERCENT > 1:
            return False, "POSITION_SIZE_PERCENT deve estar entre 0 e 1"
        
        if cls.STOP_LOSS_PERCENT <= 0:
            return False, "STOP_LOSS_PERCENT deve ser maior que 0"
        
        if cls.TAKE_PROFIT_PERCENT <= 0:
            return False, "TAKE_PROFIT_PERCENT deve ser maior que 0"
        
        return True, "Configurações válidas"
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, Any]:
        """Retorna um resumo das configurações"""
        return {
            'mode': 'TESTNET' if cls.USE_TESTNET else 'PRODUÇÃO ⚠️',
            'symbol': cls.TRADING_SYMBOL,
            'timeframe': cls.TIMEFRAME,
            'strategy': cls.STRATEGY,
            'position_size': f"{cls.POSITION_SIZE_PERCENT * 100}%",
            'stop_loss': f"{cls.STOP_LOSS_PERCENT * 100}%",
            'take_profit': f"{cls.TAKE_PROFIT_PERCENT * 100}%",
            'paper_trading': cls.PAPER_TRADING,
            'telegram': cls.ENABLE_TELEGRAM,
        }


# Instância singleton
settings = Settings()

