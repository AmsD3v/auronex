"""
Listas fixas de symbols para exchanges que não suportam modo público
"""

# Coinbase (exige API Key para markets)
COINBASE_SYMBOLS = [
    'BTC/USD', 'ETH/USD', 'SOL/USD', 'XRP/USD', 'ADA/USD',
    'DOGE/USD', 'MATIC/USD', 'LINK/USD', 'DOT/USD', 'UNI/USD',
    'AVAX/USD', 'ATOM/USD', 'LTC/USD', 'BCH/USD', 'ETC/USD',
    'FIL/USD', 'AAVE/USD', 'ALGO/USD', 'SAND/USD', 'MANA/USD',
    'CRV/USD', 'GRT/USD', 'ENJ/USD', 'BAT/USD', 'ZEC/USD'
]

# Foxbit (não existe no ccxt)
FOXBIT_SYMBOLS = [
    'BTC/BRL', 'ETH/BRL', 'XRP/BRL', 'LTC/BRL', 'BCH/BRL',
    'USDT/BRL', 'USDC/BRL', 'DOGE/BRL', 'SOL/BRL', 'MATIC/BRL'
]

# BrasilBitcoin (API instável)
BRASILBITCOIN_SYMBOLS = [
    'BTC/BRL', 'ETH/BRL', 'XRP/BRL', 'LTC/BRL', 'BCH/BRL',
    'USDT/BRL', 'DOGE/BRL', 'DASH/BRL', 'ZEC/BRL'
]

# Huobi (alguns symbols)
HUOBI_SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'SOL/USDT', 'ADA/USDT',
    'DOGE/USDT', 'MATIC/USDT', 'DOT/USDT', 'AVAX/USDT', 'LINK/USDT'
]

