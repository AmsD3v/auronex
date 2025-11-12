"""
Bot Activity Log
Retorna atividades recentes dos bots
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Trade, BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bot-activity", tags=["bot-activity"])

@router.get("/recent")
def get_recent_activity(
    db: Session = Depends(get_db)
):
    """Últimas 20 atividades dos bots (TODOS usuários - SEM AUTH)"""
    
    # Buscar trades recentes (últimas 24h)
    desde = datetime.now() - timedelta(hours=24)
    
    # ✅ TODOS os trades (não filtrar por user)
    trades = db.query(Trade).filter(
        Trade.entry_time >= desde
    ).order_by(Trade.entry_time.desc()).limit(20).all()
    
    result = []
    for trade in trades:
        bot = db.query(BotConfiguration).filter(BotConfiguration.id == trade.bot_config_id).first()
        
        # Determinar action
        if trade.status == 'open':
            action = 'buy'
        elif trade.status == 'closed':
            action = 'sell' if trade.profit_loss else 'hold'
        else:
            action = 'analyzing'
        
        result.append({
            "id": trade.id,
            "bot_id": trade.bot_config_id,
            "bot_name": bot.name if bot else "Bot",
            "timestamp": trade.entry_time.isoformat(),
            "action": action,
            "symbol": trade.symbol,
            "price": float(trade.entry_price) if trade.entry_price else None,
            "quantity": float(trade.quantity) if trade.quantity else None,
            "profit": float(trade.profit_loss) if trade.profit_loss else None,
            "reason": f"Trade #{trade.id}"
        })
    
    return result

