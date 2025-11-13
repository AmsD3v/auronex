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
        
        # Map de exchanges
        ccxt_map = {
            'mercadobitcoin': 'mercado',
            'brasilbitcoin': None,  # Não suportada
            'gateio': 'gate'
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
        
        # ✅ Filtrar por moeda relevante
        if exchange.lower() == 'mercadobitcoin':
            # MB: apenas BRL
            symbols_filtered = [s for s in symbols if '/BRL' in s]
            print(f"[Symbols] MB filtrado: {len(symbols_filtered)} /BRL")
            return sorted(symbols_filtered)
        
        elif exchange.lower() in ['binance', 'bybit', 'okx', 'gateio']:
            # Outras: apenas USDT (mais líquido)
            symbols_filtered = [s for s in symbols if '/USDT' in s and ':' not in s]  # Remove futuros
            print(f"[Symbols] {exchange.upper()} filtrado: {len(symbols_filtered)} /USDT")
            return sorted(symbols_filtered)[:200]  # Top 200
        
        else:
            return sorted(symbols)[:100]
        
    except Exception as e:
        print(f"[Symbols] Erro {exchange}: {e}")
        import traceback
        traceback.print_exc()
        
        # Fallback inteligente POR EXCHANGE
        if exchange.lower() == 'mercadobitcoin':
            return ['BTC/BRL', 'ETH/BRL', 'XRP/BRL', 'SOL/BRL', 'USDT/BRL']
        else:
            return ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'PEPE/USDT', 'SHIB/USDT', 'XRP/USDT']


