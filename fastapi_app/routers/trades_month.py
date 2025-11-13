"""
Trades do Mês - Histórico Mensal
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime

from ..database import get_db
from ..models import Trade

router = APIRouter(prefix="/api/trades", tags=["trades-month"])

@router.get("/month")
def get_trades_month(db: Session = Depends(get_db)):
    """Trades do MÊS atual (todos usuários, SEM AUTH)"""
    
    hoje = datetime.now()
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    trades = db.query(Trade).filter(
        extract('month', Trade.entry_time) == mes_atual,
        extract('year', Trade.entry_time) == ano_atual
    ).order_by(Trade.entry_time.desc()).all()
    
    result = []
    for t in trades:
        result.append({
            "id": t.id,
            "symbol": t.symbol,
            "entry_price": float(t.entry_price) if t.entry_price else 0,
            "exit_price": float(t.exit_price) if t.exit_price else 0,
            "quantity": float(t.quantity) if t.quantity else 0,
            "profit_loss": float(t.profit_loss) if t.profit_loss else 0,
            "entry_time": t.entry_time.isoformat() if t.entry_time else None,
            "exit_time": t.exit_time.isoformat() if t.exit_time else None,
            "status": t.status
        })
    
    return {
        "trades": result,
        "total": len(result),
        "mes": mes_atual,
        "ano": ano_atual
    }

