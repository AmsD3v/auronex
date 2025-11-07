"""
Endpoint para buscar saldo de um bot específico
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, BotConfiguration, ExchangeAPIKey
from ..auth import get_current_user
from ..utils.encryption import decrypt_data

router = APIRouter(prefix="/api/bots", tags=["bots-saldo"])

@router.get("/{bot_id}/saldo")
def get_bot_saldo(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar saldo REAL da corretora de um bot específico"""
    
    # Buscar bot
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    # Buscar API Key
    api_key = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == current_user.id,
        ExchangeAPIKey.exchange == bot.exchange,
        ExchangeAPIKey.is_active == True
    ).first()
    
    if not api_key:
        return {"saldo_usd": 0, "saldo_brl": 0, "erro": "API Key não configurada"}
    
    try:
        import ccxt
        
        # ✅ Mapeamento completo
        ccxt_map = {
            'mercadobitcoin': 'mercado',
            'brasilbitcoin': None,
            'gateio': 'gate',
            'foxbit': 'foxbit',
            'novadax': 'novadax',
        }
        
        ccxt_name = ccxt_map.get(bot.exchange, bot.exchange)
        
        if ccxt_name is None:
            return {"saldo_usd": 0, "saldo_brl": 0, "erro": f"{bot.exchange.upper()} não suportada"}
        
        # Conectar
        api_dec = decrypt_data(api_key.api_key_encrypted)
        secret_dec = decrypt_data(api_key.secret_key_encrypted)
        
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True,
            'timeout': 30000,
            'options': {
                'defaultType': 'spot',
                'adjustForTimeDifference': True,  # ✅ Corrigir timestamp
                'recvWindow': 60000,  # ✅ Janela maior para Bybit
            }
        })
        
        if api_key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Buscar saldo
        balance = exchange.fetch_balance()
        
        # USDT
        saldo_usdt = balance.get('free', {}).get('USDT', 0) or balance.get('USDT', {}).get('free', 0) or 0
        
        if saldo_usdt == 0:
            busd = balance.get('free', {}).get('BUSD', 0) or 0
            usdc = balance.get('free', {}).get('USDC', 0) or 0
            saldo_usdt = busd + usdc
        
        if saldo_usdt == 0:
            brl = balance.get('free', {}).get('BRL', 0) or 0
            if brl > 0:
                saldo_usdt = brl / 5.0
        
        saldo_brl = saldo_usdt * 5.0
        
        return {
            "saldo_usd": round(saldo_usdt, 2),
            "saldo_brl": round(saldo_brl, 2),
            "exchange": bot.exchange.upper()
        }
        
    except Exception as e:
        return {"saldo_usd": 0, "saldo_brl": 0, "erro": str(e)[:100]}





