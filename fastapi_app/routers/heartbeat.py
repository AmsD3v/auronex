"""
Heartbeat e Session Management
Detecta quando navegador fecha e DESATIVA bots automaticamente
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import User, BotConfiguration
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["heartbeat"])

# Cache de heartbeats {user_id: timestamp}
heartbeats = {}

@router.post("/heartbeat")
def heartbeat(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Recebe heartbeat do frontend (a cada 30s)
    Atualiza timestamp do usuário
    """
    heartbeats[current_user.id] = datetime.now().timestamp()
    return {"status": "ok"}

@router.post("/session/close")
def session_close(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ✅ CRÍTICO: Chamado ao fechar navegador
    DESATIVA todos os bots do usuário
    """
    
    # Desativar TODOS os bots do usuário
    bots = db.query(BotConfiguration).filter(
        BotConfiguration.user_id == current_user.id,
        BotConfiguration.is_active == True
    ).all()
    
    for bot in bots:
        bot.is_active = False
    
    db.commit()
    
    # Remover heartbeat
    if current_user.id in heartbeats:
        del heartbeats[current_user.id]
    
    print(f"")
    print(f"{'🚪'*30}")
    print(f"[SESSION CLOSE] Usuário {current_user.email} fechou navegador")
    print(f"[SESSION CLOSE] {len(bots)} bot(s) DESATIVADO(S) automaticamente")
    print(f"{'🚪'*30}")
    
    return {
        "status": "session_closed",
        "bots_stopped": len(bots)
    }

@router.get("/session/check-inactive")
def check_inactive_sessions(db: Session = Depends(get_db)):
    """
    Verifica sessões sem heartbeat há 60s+
    Desativa bots de usuários inativos
    """
    import time
    
    now = time.time()
    inactive_users = []
    
    for user_id, last_heartbeat in list(heartbeats.items()):
        if now - last_heartbeat > 60:  # 60s sem heartbeat
            inactive_users.append(user_id)
    
    # Desativar bots
    bots_stopped = 0
    for user_id in inactive_users:
        bots = db.query(BotConfiguration).filter(
            BotConfiguration.user_id == user_id,
            BotConfiguration.is_active == True
        ).all()
        
        for bot in bots:
            bot.is_active = False
            bots_stopped += 1
        
        del heartbeats[user_id]
    
    if bots_stopped > 0:
        db.commit()
        print(f"[SESSION] {bots_stopped} bot(s) desativado(s) por inatividade")
    
    return {
        "inactive_users": len(inactive_users),
        "bots_stopped": bots_stopped
    }

