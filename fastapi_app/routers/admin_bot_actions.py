"""
Admin Bot Actions - SEM AUTH (para admin HTML)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import BotConfiguration

router = APIRouter(prefix="/api/admin/bot-actions", tags=["admin-bot-actions"])

@router.delete("/{bot_id}")
def admin_delete_bot(bot_id: int, db: Session = Depends(get_db)):
    """Admin deletar bot (SEM AUTH)"""
    
    bot = db.query(BotConfiguration).filter(BotConfiguration.id == bot_id).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    db.delete(bot)
    db.commit()
    
    print(f"[Admin] Bot {bot_id} deletado")
    
    return {"message": "Bot deletado", "bot_id": bot_id}

@router.patch("/{bot_id}/toggle")
def admin_toggle_bot(bot_id: int, db: Session = Depends(get_db)):
    """Admin ativar/desativar bot (SEM AUTH)"""
    
    bot = db.query(BotConfiguration).filter(BotConfiguration.id == bot_id).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    # Toggle
    bot.is_active = not bot.is_active
    bot.updated_at = datetime.utcnow()
    
    db.commit()
    
    print(f"[Admin] Bot {bot_id}: is_active={bot.is_active}")
    
    return {"message": f"Bot {'ativado' if bot.is_active else 'desativado'}", "is_active": bot.is_active}

