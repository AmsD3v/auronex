"""
API de estatísticas de trades
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..database import get_db
from ..models import Trade, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/trades", tags=["trades-stats"])

@router.get("/today")
def get_trades_today(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Trades realizados hoje"""
    
    hoje = datetime.now().date()
    
    count = db.query(Trade).filter(
        Trade.user_id == current_user.id,
        func.date(Trade.entry_time) == hoje
    ).count()
    
    return {"count": count, "date": str(hoje)}

@router.get("/stats")
def get_trade_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Estatísticas de trades (win rate)"""
    
    # Trades fechados (com lucro/perda)
    trades = db.query(Trade).filter(
        Trade.user_id == current_user.id,
        Trade.exit_time.isnot(None)
    ).all()
    
    total_trades = len(trades)
    
    if total_trades == 0:
        return {
            "total_trades": 0,
            "win_trades": 0,
            "loss_trades": 0,
            "win_rate": 0
        }
    
    # Contar wins e losses
    win_trades = sum(1 for t in trades if t.profit_loss and t.profit_loss > 0)
    loss_trades = total_trades - win_trades
    
    win_rate = (win_trades / total_trades * 100) if total_trades > 0 else 0
    
    # ✅ Calcular lucro/perda TOTAL
    total_profit = sum(t.profit_loss for t in trades if t.profit_loss) or 0
    
    return {
        "total_trades": total_trades,
        "win_trades": win_trades,
        "loss_trades": loss_trades,
        "win_rate": round(win_rate, 2),
        "total_profit": round(total_profit, 2)  # ✅ Lucro líquido!
    }






