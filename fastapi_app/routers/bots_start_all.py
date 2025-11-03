"""
Endpoint para iniciar todos os bots do usuário
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import BotConfiguration, User
from ..auth import get_current_user

router = APIRouter(prefix="/api/bots", tags=["bots-start-all"])

@router.post("/start-all")
def start_all_bots(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Iniciar todos os bots do usuário"""
    
    try:
        # Buscar todos os bots do usuário
        bots = db.query(BotConfiguration).filter(
            BotConfiguration.user_id == current_user.id
        ).all()
        
        activated = 0
        
        for bot in bots:
            if not bot.is_active:
                bot.is_active = True
                bot.updated_at = datetime.utcnow()
                activated += 1
        
        db.commit()
        
        print(f"✅ {activated} bot(s) iniciado(s) para usuário {current_user.id}")
        
        return {
            "success": True,
            "activated": activated,
            "total": len(bots)
        }
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao iniciar bots: {str(e)}")
        return {"success": False, "error": str(e)}




