"""Exchange endpoints - LIMPO E FUNCIONAL"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, ExchangeAPIKey
from ..auth import get_current_user
from ..utils.encryption import decrypt_data

router = APIRouter(prefix="/api/exchange", tags=["exchange"])

@router.get("/balance")
def get_balance(
    exchange: str = Query(default=None),
    db: Session = Depends(get_db)
):
    """
    Buscar saldo (SEM AUTH para dashboard funcionar)
    - Se exchange específica: retorna saldo dela
    - Sem exchange: retorna saldo TOTAL de TODAS as exchanges
    
    ⚠️ SEM USER = retorna saldo de TODAS API keys do sistema
    """
    
    # ✅ Se especificou exchange, buscar dela (PRIMEIRA ativa do sistema)
    if exchange:
        api_key = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.exchange == exchange.lower(),
            ExchangeAPIKey.is_active == True
        ).first()
    else:
        # ✅ SEM exchange = SOMAR TODAS as exchanges do sistema!
        api_keys = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.is_active == True
        ).all()
        
        if not api_keys:
            return {
                "usdt": 0,
                "btc": 0,
                "eth": 0,
                "bnb": 0,
                "total_usd": 0,
                "exchange": "none",
                "is_testnet": True
            }
        
        # Somar TODAS as exchanges
        total_usdt = 0
        
        for api_key in api_keys:
            try:
                import ccxt
                ccxt_map = {
                    'mercadobitcoin': 'mercado',
                    'brasilbitcoin': None,  # Não suportada
                    'gateio': 'gate'
                }
                ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
                
                if ccxt_name is None:
                    continue  # Pular exchange não suportada
                
                api_dec = decrypt_data(api_key.api_key_encrypted)
                secret_dec = decrypt_data(api_key.secret_key_encrypted)
                
                exchange_class = getattr(ccxt, ccxt_name)
                exchange_obj = exchange_class({
                    'apiKey': api_dec,
                    'secret': secret_dec,
                    'enableRateLimit': True,
                })
                
                if api_key.is_testnet:
                    exchange_obj.set_sandbox_mode(True)
                
                balance = exchange_obj.fetch_balance()
                usdt = balance.get('free', {}).get('USDT', 0) or 0
                
                # ✅ Se 0, tentar BRL (exchanges brasileiras)
                if usdt == 0:
                    brl = balance.get('free', {}).get('BRL', 0) or 0
                    if brl > 0:
                        usdt = brl / 5.0  # Converter
                        print(f"[Balance] {api_key.exchange.upper()}: R$ {brl:.2f} = ${usdt:.2f}")
                
                total_usdt += usdt
                
                if usdt > 0:
                    print(f"[Balance] {api_key.exchange.upper()}: ${usdt:.2f}")
                
            except:
                pass
        
        print(f"[Balance TOTAL] ${total_usdt:.2f} de {len(api_keys)} exchange(s)")
        
        return {
            "usdt": round(total_usdt, 2),
            "btc": 0,
            "eth": 0,
            "bnb": 0,
            "total_usd": round(total_usdt, 2),
            "exchange": "consolidated",
            "is_testnet": True
        }
    
    # Exchange específica
    api_key = api_key
    
    if not api_key:
        # ✅ Retornar saldo 0 ao invés de erro
        return {
            "usdt": 0,
            "btc": 0,
            "eth": 0,
            "bnb": 0,
            "total_usd": 0,
            "exchange": exchange or "none",
            "is_testnet": True,
            "error": "API Key não configurada"
        }
    
    try:
        import ccxt
        
        ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate', 'foxbit': 'foxbit', 'novadax': 'novadax'}
        ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
        
        api_dec = decrypt_data(api_key.api_key_encrypted)
        secret_dec = decrypt_data(api_key.secret_key_encrypted)
        
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True,
            'options': {'defaultType': 'spot', 'adjustForTimeDifference': True}
        })
        
        if api_key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        balance = exchange.fetch_balance()
        
        usdt = balance.get('free', {}).get('USDT', 0) or 0
        
        # ✅ Se 0, tentar BRL
        if usdt == 0:
            brl = balance.get('free', {}).get('BRL', 0) or 0
            if brl > 0:
                usdt = brl / 5.0
        
        btc = balance.get('free', {}).get('BTC', 0) or 0
        eth = balance.get('free', {}).get('ETH', 0) or 0
        bnb = balance.get('free', {}).get('BNB', 0) or 0
        
        return {
            "usdt": round(usdt, 2),
            "btc": round(btc, 8),
            "eth": round(eth, 6),
            "bnb": round(bnb, 4),
            "total_usd": round(usdt, 2),
            "exchange": api_key.exchange.upper(),
            "is_testnet": api_key.is_testnet
        }
        
    except Exception as e:
        print(f"[Balance] ERRO: {str(e)[:200]}")
        # ✅ Retornar saldo 0 ao invés de erro 500
        return {
            "usdt": 0,
            "btc": 0,
            "eth": 0,
            "bnb": 0,
            "total_usd": 0,
            "exchange": exchange or "unknown",
            "is_testnet": True,
            "error": "Erro ao conectar exchange (Testnet offline?)"
        }

@router.get("/symbols")
def get_symbols(
    exchange: str = Query(default="binance")
):
    """
    Buscar símbolos PÚBLICOS da exchange (SEM API KEY necessária!)
    
    ✅ Cliente pode ver cryptos ANTES de criar conta
    ✅ Não precisa API Key para listar
    ✅ Usa ccxt em modo público
    """
    
    try:
        import ccxt
        
        # Map de exchanges (ccxt usa nomes diferentes)
        ccxt_map = {
            'mercadobitcoin': 'mercado',
            'brasilbitcoin': 'brasilbitcoin',  # ✅ Suportada!
            'gateio': 'gate',
            'foxbit': 'foxbit',
            'huobi': 'huobi',
            # Coinbase já tem nome correto
        }
        
        ccxt_name = ccxt_map.get(exchange.lower(), exchange.lower())
        
        if ccxt_name is None:
            return []  # Exchange não suportada
        
        # ✅ Criar exchange em MODO PÚBLICO (sem API Key!)
        exchange_class = getattr(ccxt, ccxt_name)
        exchange_obj = exchange_class({
            'enableRateLimit': True,
            # ✅ SEM apiKey/secret = modo público!
        })
        
        # ✅ Carregar markets PUBLICAMENTE (não precisa auth!)
        markets = exchange_obj.load_markets()
        
        # Pegar symbols
        symbols = list(markets.keys())
        
        print(f"[Symbols PÚBLICO] {exchange.upper()}: {len(symbols)} símbolos")
        
        # ✅ Filtrar por moeda relevante POR EXCHANGE
        exchange_lower = exchange.lower()
        
        # Exchanges brasileiras: apenas BRL
        if exchange_lower in ['mercadobitcoin', 'brasilbitcoin', 'foxbit']:
            symbols_filtered = [s for s in symbols if '/BRL' in s and ':' not in s]
            print(f"[Symbols] {exchange.upper()} /BRL: {len(symbols_filtered)}")
            return sorted(symbols_filtered)
        
        # Exchanges internacionais: USDT (spot) + USD (algumas)
        elif exchange_lower in ['binance', 'bybit', 'okx', 'gateio', 'huobi']:
            # USDT (spot apenas, sem futuros)
            symbols_usdt = [s for s in symbols if '/USDT' in s and ':' not in s]
            print(f"[Symbols] {exchange.upper()} /USDT: {len(symbols_usdt)}")
            return sorted(symbols_usdt)
        
        # Coinbase: USD
        elif exchange_lower == 'coinbase':
            symbols_usd = [s for s in symbols if '/USD' in s and ':' not in s]
            print(f"[Symbols] COINBASE /USD: {len(symbols_usd)}")
            return sorted(symbols_usd)
        
        # Kraken: USD e USDT
        elif exchange_lower == 'kraken':
            symbols_filtered = [s for s in symbols if ('/USD' in s or '/USDT' in s) and ':' not in s]
            print(f"[Symbols] KRAKEN /USD+/USDT: {len(symbols_filtered)}")
            return sorted(symbols_filtered)
        
        # Outras: retornar tudo
        else:
            print(f"[Symbols] {exchange.upper()} TODAS: {len(symbols)}")
            return sorted(symbols)
        
    except Exception as e:
        print(f"[Symbols] Erro {exchange}: {e}")
        
        # ✅ Fallback com listas FIXAS (exchanges sem modo público)
        from ..data.exchange_symbols import (
            COINBASE_SYMBOLS, FOXBIT_SYMBOLS, BRASILBITCOIN_SYMBOLS, HUOBI_SYMBOLS
        )
        
        exchange_lower = exchange.lower()
        
        if exchange_lower == 'coinbase':
            print(f"[Symbols] Usando lista fixa Coinbase: {len(COINBASE_SYMBOLS)}")
            return COINBASE_SYMBOLS
        
        elif exchange_lower == 'foxbit':
            print(f"[Symbols] Usando lista fixa Foxbit: {len(FOXBIT_SYMBOLS)}")
            return FOXBIT_SYMBOLS
        
        elif exchange_lower == 'brasilbitcoin':
            print(f"[Symbols] Usando lista fixa BrasilBitcoin: {len(BRASILBITCOIN_SYMBOLS)}")
            return BRASILBITCOIN_SYMBOLS
        
        elif exchange_lower == 'huobi':
            print(f"[Symbols] Usando lista fixa Huobi: {len(HUOBI_SYMBOLS)}")
            return HUOBI_SYMBOLS
        
        # Fallback genérico
        elif 'brasil' in exchange_lower or 'mercado' in exchange_lower:
            return ['BTC/BRL', 'ETH/BRL', 'XRP/BRL', 'SOL/BRL', 'USDT/BRL']
        else:
            return ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT']


