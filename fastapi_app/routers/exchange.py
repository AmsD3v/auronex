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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar saldo
    - Se exchange específica: retorna saldo dela
    - Sem exchange: retorna saldo TOTAL de TODAS as exchanges
    """
    
    # ✅ Se especificou exchange, buscar dela
    if exchange:
        api_key = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == current_user.id,
            ExchangeAPIKey.exchange == exchange.lower(),
            ExchangeAPIKey.is_active == True
        ).first()
    else:
        # ✅ SEM exchange = SOMAR TODAS!
        api_keys = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == current_user.id,
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
                ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate'}
                ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
                
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
                
                total_usdt += usdt
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
    exchange: str = Query(default="binance"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar símbolos"""
    # Lista padrão grande
    return [
        'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT', 'XRP/USDT',
        'DOT/USDT', 'DOGE/USDT', 'MATIC/USDT', 'AVAX/USDT', 'LINK/USDT', 'UNI/USDT',
        'ATOM/USDT', 'LTC/USDT', 'GALA/USDT', 'PEPE/USDT', 'SHIB/USDT'
    ]

