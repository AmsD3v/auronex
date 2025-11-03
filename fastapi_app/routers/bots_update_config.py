"""
API para atualizar configurações dinâmicas do bot
Estratégia, modo, velocidade, etc
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from ..database import get_db
from ..models import BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bots", tags=["bots-config"])

class UpdateBotConfig(BaseModel):
    strategy: Optional[str] = None
    modo_cacador: Optional[bool] = None
    velocidade_analise: Optional[int] = None

@router.patch("/{bot_id}/config")
def update_bot_config(
    bot_id: int,
    data: UpdateBotConfig,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza configuração dinâmica do bot"""
    
    # Buscar bot
    bot = db.query(BotConfiguration).filter(
        BotConfiguration.id == bot_id,
        BotConfiguration.user_id == current_user.id
    ).first()
    
    if not bot:
        raise HTTPException(status_code=404, detail="Bot não encontrado")
    
    # Atualizar campos
    if data.strategy:
        bot.strategy = data.strategy
        print(f"[OK] Bot {bot_id}: Estratégia → {data.strategy}")
    
    if data.modo_cacador is not None:
        # Salvar em campo extra (JSON)
        # Por enquanto, alterar strategy
        if data.modo_cacador:
            bot.strategy = 'hunter'  # Modo caçador
            print(f"[OK] Bot {bot_id}: Modo CAÇADOR ativado!")
        else:
            bot.strategy = 'mean_reversion'  # Voltar padrão
            print(f"[OK] Bot {bot_id}: Modo caçador desativado")
    
    bot.updated_at = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "bot_id": bot_id,
        "strategy": bot.strategy
    }


