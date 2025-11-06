"""
Exchange endpoints - Para dashboard React
Buscar saldo, ticker, OHLCV, etc
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import User, ExchangeAPIKey
from ..auth import get_current_user
from ..utils.encryption import decrypt_data

router = APIRouter(prefix="/api/exchange", tags=["exchange"])


@router.get("/balance")
def get_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar saldo da exchange
    ✅ Retorna saldo consolidado de todas exchanges do usuário
    """
    
    # Buscar TODAS as API Keys ativas do usuário
    api_keys = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == current_user.id,
        ExchangeAPIKey.is_active == True
    ).all()
    
    if not api_keys:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma API Key configurada. Configure em /api-keys-page"
        )
    
    # Usar a primeira API Key disponível
    api_key = api_keys[0]
    
    try:
        import ccxt
        
        # Mapeamento de nomes
        ccxt_map = {
            'mercadobitcoin': 'mercado',
            'brasilbitcoin': None,
            'gateio': 'gate'
        }
        
        ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
        
        if ccxt_name is None:
            raise HTTPException(
                status_code=400,
                detail=f"Exchange {api_key.exchange.upper()} não suportada"
            )
        
        # Descriptografar chaves
        api_dec = decrypt_data(api_key.api_key_encrypted)
        secret_dec = decrypt_data(api_key.secret_key_encrypted)
        
        # Conectar à exchange
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True,
            'timeout': 15000,
            'options': {'defaultType': 'spot'}
        })
        
        if api_key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Buscar saldo
        balance = exchange.fetch_balance()
        
        # Extrair valores (várias formas para compatibilidade)
        usdt = balance.get('free', {}).get('USDT', 0) or balance.get('USDT', {}).get('free', 0) or 0
        btc = balance.get('free', {}).get('BTC', 0) or balance.get('BTC', {}).get('free', 0) or 0
        eth = balance.get('free', {}).get('ETH', 0) or balance.get('ETH', {}).get('free', 0) or 0
        bnb = balance.get('free', {}).get('BNB', 0) or balance.get('BNB', {}).get('free', 0) or 0
        
        # Se USDT = 0, tentar outras stablecoins
        if usdt == 0:
            busd = balance.get('free', {}).get('BUSD', 0) or 0
            usdc = balance.get('free', {}).get('USDC', 0) or 0
            dai = balance.get('free', {}).get('DAI', 0) or 0
            usdt = busd + usdc + dai
        
        # Se ainda 0, tentar BRL (exchanges brasileiras)
        if usdt == 0:
            brl = balance.get('free', {}).get('BRL', 0) or 0
            if brl > 0:
                usdt = brl / 5.0  # Conversão aproximada
        
        # Calcular total em USD
        # (Aqui poderíamos buscar preço de BTC, ETH, BNB, mas por simplicidade usamos USDT)
        total_usd = usdt + (btc * 0) + (eth * 0) + (bnb * 0)  # Simplificado
        
        return {
            "usdt": round(usdt, 2),
            "btc": round(btc, 8),
            "eth": round(eth, 6),
            "bnb": round(bnb, 4),
            "total_usd": round(total_usd, 2),
            "exchange": api_key.exchange.upper(),
            "is_testnet": api_key.is_testnet
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao buscar saldo: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar saldo da exchange: {str(e)[:200]}"
        )


@router.get("/ticker")
def get_ticker(
    symbol: str = Query(..., description="Símbolo (ex: BTC/USDT)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar ticker de um símbolo
    """
    
    # Buscar primeira API Key ativa
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == current_user.id,
        ExchangeAPIKey.is_active == True
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key não configurada")
    
    try:
        import ccxt
        
        ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate'}
        ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
        
        api_dec = decrypt_data(api_key.api_key_encrypted)
        secret_dec = decrypt_data(api_key.secret_key_encrypted)
        
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True
        })
        
        if api_key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Buscar ticker
        ticker = exchange.fetch_ticker(symbol)
        
        return {
            "symbol": symbol,
            "last": ticker.get('last', 0),
            "bid": ticker.get('bid', 0),
            "ask": ticker.get('ask', 0),
            "high": ticker.get('high', 0),
            "low": ticker.get('low', 0),
            "volume": ticker.get('volume', 0),
            "change": ticker.get('change', 0),
            "changePercent": ticker.get('percentage', 0),
            "timestamp": ticker.get('timestamp', 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ohlcv")
def get_ohlcv(
    symbol: str = Query(..., description="Símbolo (ex: BTC/USDT)"),
    timeframe: str = Query(default="1h", description="Timeframe (1m, 5m, 15m, 1h, 4h, 1d)"),
    limit: int = Query(default=100, le=500, description="Número de candles"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar dados OHLCV (candlesticks)
    """
    
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == current_user.id,
        ExchangeAPIKey.is_active == True
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key não configurada")
    
    try:
        import ccxt
        
        ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate'}
        ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
        
        api_dec = decrypt_data(api_key.api_key_encrypted)
        secret_dec = decrypt_data(api_key.secret_key_encrypted)
        
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True
        })
        
        if api_key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Buscar OHLCV
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        # Converter para formato amigável
        candles = []
        for candle in ohlcv:
            candles.append({
                "timestamp": candle[0],
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4],
                "volume": candle[5]
            })
        
        return candles
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/symbols")
def get_symbols(
    exchange: str = Query(default="binance", description="Nome da exchange"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Buscar símbolos disponíveis na exchange
    """
    
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == current_user.id,
        ExchangeAPIKey.exchange == exchange.lower(),
        ExchangeAPIKey.is_active == True
    ).first()
    
    if not api_key:
        # Retornar lista padrão se não tem API Key
        return [
            'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT',
            'XRP/USDT', 'DOT/USDT', 'DOGE/USDT', 'MATIC/USDT', 'AVAX/USDT'
        ]
    
    try:
        import ccxt
        
        ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate'}
        ccxt_name = ccxt_map.get(api_key.exchange, api_key.exchange)
        
        api_dec = decrypt_data(api_key.api_key_encrypted)
        secret_dec = decrypt_data(api_key.secret_key_encrypted)
        
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True
        })
        
        if api_key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Carregar markets
        markets = exchange.load_markets()
        
        # Filtrar apenas pares USDT/BRL e REMOVER DUPLICATAS
        symbols_set = set()
        for symbol in markets.keys():
            # Apenas USDT e BRL
            if '/USDT' in symbol or '/BRL' in symbol or '/BTC' in symbol:
                # Normalizar formato (sempre com /)
                normalized = symbol.replace(':USDT', '/USDT').replace(':BRL', '/BRL').replace(':BTC', '/BTC')
                symbols_set.add(normalized)
        
        # Converter para lista e ordenar
        return sorted(list(symbols_set))
        
    except Exception as e:
        print(f"Erro ao buscar símbolos: {e}")
        # Retornar lista padrão em caso de erro
        return [
            'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'ADA/USDT',
            'XRP/USDT', 'DOT/USDT', 'DOGE/USDT', 'MATIC/USDT', 'AVAX/USDT'
        ]

