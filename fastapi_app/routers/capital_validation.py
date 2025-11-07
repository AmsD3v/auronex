"""
Validação de Capital Alocado
Capital total dos bots NÃO pode ultrapassar saldo disponível
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, BotConfiguration, ExchangeAPIKey
from ..auth import get_current_user
from ..utils.encryption import decrypt_data

router = APIRouter(prefix="/api/capital", tags=["capital"])

@router.get("/validation")
def validate_capital(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Valida capital alocado vs saldo disponível
    
    Returns:
        {
            "saldo_total_usd": float,
            "capital_alocado_usd": float,
            "capital_disponivel_usd": float,
            "pode_alocar": bool,
            "detalhes": [...]
        }
    """
    
    # Buscar todos os bots do usuário
    bots = db.query(BotConfiguration).filter(
        BotConfiguration.user_id == current_user.id
    ).all()
    
    # Calcular capital alocado (apenas bots ATIVOS)
    capital_alocado = sum(
        float(bot.capital) for bot in bots 
        if bot.is_active and bot.capital
    )
    
    # Buscar saldo total de TODAS exchanges
    saldo_total = 0
    detalhes_exchanges = []
    
    # Pegar exchanges únicas dos bots ativos
    exchanges_ativas = list(set([bot.exchange for bot in bots if bot.is_active]))
    
    for exchange_name in exchanges_ativas:
        api_key = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == current_user.id,
            ExchangeAPIKey.exchange == exchange_name,
            ExchangeAPIKey.is_active == True
        ).first()
        
        if not api_key:
            continue
        
        try:
            import ccxt
            
            ccxt_map = {
                'mercadobitcoin': 'mercado',
                'gateio': 'gate',
                'foxbit': 'foxbit',
                'novadax': 'novadax',
            }
            ccxt_name = ccxt_map.get(exchange_name, exchange_name)
            
            if ccxt_name is None:
                continue
            
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
                    'adjustForTimeDifference': True,
                    'recvWindow': 60000,
                }
            })
            
            if api_key.is_testnet:
                exchange.set_sandbox_mode(True)
            
            balance = exchange.fetch_balance()
            usdt = balance.get('free', {}).get('USDT', 0) or 0
            
            saldo_total += usdt
            detalhes_exchanges.append({
                'exchange': exchange_name.upper(),
                'saldo': usdt
            })
            
        except Exception as e:
            print(f"[Capital] Erro ao buscar saldo {exchange_name}: {e}")
    
    capital_disponivel = saldo_total - capital_alocado
    pode_alocar = capital_disponivel > 0
    
    print(f"[Capital] Saldo: ${saldo_total:.2f} | Alocado: ${capital_alocado:.2f} | Disponível: ${capital_disponivel:.2f}")
    
    return {
        "saldo_total_usd": round(saldo_total, 2),
        "capital_alocado_usd": round(capital_alocado, 2),
        "capital_disponivel_usd": round(capital_disponivel, 2),
        "pode_alocar": pode_alocar,
        "porcentagem_alocada": (capital_alocado / saldo_total * 100) if saldo_total > 0 else 0,
        "detalhes": detalhes_exchanges,
        "bots_ativos": len([b for b in bots if b.is_active])
    }


