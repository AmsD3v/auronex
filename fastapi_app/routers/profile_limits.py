"""
Endpoint de limites do plano do usuário
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..auth import get_current_user

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/limits/")
def get_user_limits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retornar limites do plano do usuário"""
    
    # Buscar assinatura ativa
    try:
        from ..models_payment import Subscription
        
        subscription = db.query(Subscription).filter(
            Subscription.user_id == current_user.id,
            Subscription.status == "active"
        ).order_by(Subscription.id.desc()).first()
        
        if not subscription:
            plan = "free"
        else:
            plan = subscription.plan
            
    except:
        plan = "free"
    
    # Definir limites por plano - ATUALIZADO 06/11/2025
    limits = {
        "free": {
            "plan": "free",
            "max_bots": 1,
            "max_api_keys": 1,
            "max_capital_per_bot": 100,
            "max_symbols_per_bot": 1,
            "trial_days": 3  # ✅ 3 dias de teste (era 7)
        },
        "pro": {
            "plan": "pro",
            "max_bots": 3,  # ✅ 3 bots (era 5)
            "max_api_keys": 3,
            "max_capital_per_bot": 1000,
            "max_symbols_per_bot": 2,  # ✅ 2 cryptos (era 3)
            "price_brl": 29.90,
            "price_usd": 5.99
        },
        "premium": {
            "plan": "premium",
            "max_bots": 5,  # ✅ 5 bots (era 10)
            "max_api_keys": 10,
            "max_capital_per_bot": 10000,
            "max_symbols_per_bot": 3,  # ✅ 3 cryptos (era 5)
            "price_brl": 59.90,  # ✅ R$ 59,90 (era 99,90)
            "price_usd": 11.99
        }
    }
    
    return limits.get(plan, limits["free"])

