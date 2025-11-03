"""
Router de Trades - Histórico de operações
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..models import Trade, User
from ..schemas import TradeResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/trades", tags=["trades"])

@router.get("/", response_model=List[TradeResponse])
def list_trades(
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar trades do usuário"""
    
    query = db.query(Trade).filter(Trade.user_id == current_user.id)
    
    # Filtrar por status se fornecido
    if status:
        query = query.filter(Trade.status == status)
    
    # Ordenar por mais recente
    query = query.order_by(Trade.entry_time.desc())
    
    # Paginação
    trades = query.offset(offset).limit(limit).all()
    
    return trades

@router.get("/{trade_id}/", response_model=TradeResponse)
def get_trade(
    trade_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter detalhes de um trade específico"""
    
    trade = db.query(Trade).filter(
        Trade.id == trade_id,
        Trade.user_id == current_user.id
    ).first()
    
    if not trade:
        raise HTTPException(status_code=404, detail="Trade não encontrado")
    
    return trade


