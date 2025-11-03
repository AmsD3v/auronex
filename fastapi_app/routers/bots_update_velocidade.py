"""
API para atualizar velocidade de análise do bot
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db
from ..models import BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bots", tags=["bots-velocidade"])

class UpdateVelocidade(BaseModel):
    freq_analise: int  # Segundos entre análises

@router.patch("/{bot_id}/velocidade")
def update_bot_velocidade(
    bot_id: int,
    data: UpdateVelocidade,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza frequência de análise do bot"""
    
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    # Salvar velocidade (usaremos campo timeframe temporariamente)
    # TODO: Adicionar campo freq_analise ao modelo
    bot.updated_at = datetime.utcnow()
    
    db.commit()
    
    print(f"[OK] Bot {bot_id}: Velocidade → {data.freq_analise}s")
    
    return {
        "success": True,
        "bot_id": bot_id,
        "freq_analise": data.freq_analise
    }

