"""
Endpoint para buscar um bot específico
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bots", tags=["bots-get"])

@router.get("/{bot_id}")
def get_bot(
    bot_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar bot específico do usuário"""
    
    try:
        bot = db.query(BotConfiguration).filter(
            BotConfiguration.id == bot_id,
            BotConfiguration.user_id == current_user.id
        ).first()
        
        if not bot:
            raise HTTPException(status_code=404, detail="Bot não encontrado")
        
        # Retornar dict manual
        return {
            "id": bot.id,
            "name": bot.name,
            "exchange": bot.exchange,
            "symbols": bot.symbols if isinstance(bot.symbols, list) else [bot.symbols],
            "capital": float(bot.capital) if bot.capital else 0,
            "strategy": bot.strategy,
            "timeframe": bot.timeframe,
            "stop_loss_percent": float(bot.stop_loss_percent) if bot.stop_loss_percent else 0,
            "take_profit_percent": float(bot.take_profit_percent) if bot.take_profit_percent else 0,
            "is_active": bot.is_active
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao buscar bot: {e}")
        raise HTTPException(status_code=500, detail=str(e))


