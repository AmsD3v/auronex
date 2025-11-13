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

# Foxbit (100+ cryptos baseado em pesquisa)
FOXBIT_SYMBOLS = [
    # Principais (Top 30)
    'BTC/BRL', 'ETH/BRL', 'USDT/BRL', 'BNB/BRL', 'XRP/BRL', 'ADA/BRL', 'SOL/BRL', 'DOGE/BRL',
    'DOT/BRL', 'MATIC/BRL', 'SHIB/BRL', 'UNI/BRL', 'LINK/BRL', 'AVAX/BRL', 'ATOM/BRL',
    'LTC/BRL', 'BCH/BRL', 'XLM/BRL', 'ALGO/BRL', 'VET/BRL', 'FIL/BRL', 'TRX/BRL',
    'ETC/BRL', 'THETA/BRL', 'XMR/BRL', 'EOS/BRL', 'AAVE/BRL', 'GRT/BRL', 'SAND/BRL', 'MANA/BRL',
    
    # Adicionais (70+)
    'CRV/BRL', 'COMP/BRL', 'SUSHI/BRL', 'YFI/BRL', 'SNX/BRL', 'BAT/BRL', 'ZRX/BRL', 'ENJ/BRL',
    'CHZ/BRL', 'HOT/BRL', 'ZIL/BRL', 'OMG/BRL', 'ANKR/BRL', 'WAVES/BRL', 'ICX/BRL', 'ONT/BRL',
    'ZEC/BRL', 'DASH/BRL', 'QTUM/BRL', 'DCR/BRL', 'RVN/BRL', 'DGB/BRL', 'SC/BRL', 'LSK/BRL',
    'ARK/BRL', 'STRAT/BRL', 'KMD/BRL', 'AMP/BRL', 'FET/BRL', 'OCEAN/BRL', 'NMR/BRL', 'STORJ/BRL',
    'SKL/BRL', 'NU/BRL', 'BAND/BRL', 'BAL/BRL', 'REN/BRL', 'LRC/BRL', 'KNC/BRL', 'REP/BRL',
    'CELR/BRL', 'CTK/BRL', 'PERL/BRL', 'TRB/BRL', 'POLS/BRL', 'MDX/BRL', 'MIR/BRL', 'REEF/BRL',
    'OGN/BRL', 'NKN/BRL', 'LTO/BRL', 'RSR/BRL', 'OCEAN/BRL', 'DENT/BRL', 'KEY/BRL', 'STMX/BRL',
    '1INCH/BRL', 'API3/BRL', 'BADGER/BRL', 'FTM/BRL', 'LIT/BRL', 'NEAR/BRL', 'ROSE/BRL', 'SFP/BRL',
    'TLM/BRL', 'WIN/BRL', 'WRX/BRL', 'ALPHA/BRL', 'AUDIO/BRL', 'BAKE/BRL', 'C98/BRL', 'CAKE/BRL',
]

# BrasilBitcoin (40+ cryptos baseado em pesquisa)
BRASILBITCOIN_SYMBOLS = [
    # Principais
    'BTC/BRL', 'ETH/BRL', 'USDT/BRL', 'XRP/BRL', 'ADA/BRL', 'SOL/BRL', 'DOGE/BRL', 'DOT/BRL',
    'MATIC/BRL', 'UNI/BRL', 'LINK/BRL', 'LTC/BRL', 'BCH/BRL', 'XLM/BRL', 'ATOM/BRL', 'AVAX/BRL',
    
    # Adicionais
    'ALGO/BRL', 'VET/BRL', 'FIL/BRL', 'TRX/BRL', 'ETC/BRL', 'THETA/BRL', 'XMR/BRL', 'EOS/BRL',
    'AAVE/BRL', 'GRT/BRL', 'SAND/BRL', 'MANA/BRL', 'CRV/BRL', 'COMP/BRL', 'SUSHI/BRL', 'BAT/BRL',
    'ZRX/BRL', 'ENJ/BRL', 'CHZ/BRL', 'ZIL/BRL', 'ZEC/BRL', 'DASH/BRL', 'QTUM/BRL', 'WAVES/BRL',
]

# Huobi (alguns symbols)
HUOBI_SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'SOL/USDT', 'ADA/USDT',
    'DOGE/USDT', 'MATIC/USDT', 'DOT/USDT', 'AVAX/USDT', 'LINK/USDT'
]

