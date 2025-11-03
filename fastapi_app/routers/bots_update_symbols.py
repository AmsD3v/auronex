"""
API para atualizar símbolos (cryptos) de um bot
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bots", tags=["bots-symbols"])

class UpdateSymbols(BaseModel):
    symbols: List[str]

@router.patch("/{bot_id}/symbols")
def update_bot_symbols(
    bot_id: int,
    data: UpdateSymbols,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza símbolos (cryptos) de um bot"""
    
    # Buscar bot
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    # Atualizar símbolos
    bot.symbols = data.symbols
    bot.updated_at = datetime.utcnow()
    
    db.commit()
    
    print(f"[OK] Símbolos do bot {bot_id} atualizados: {data.symbols}")
    
    return {
        "success": True,
        "bot_id": bot_id,
        "symbols": data.symbols
    }


