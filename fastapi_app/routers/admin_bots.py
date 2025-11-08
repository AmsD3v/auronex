"""
Admin - Bots
Gerenciar TODOS os bots do sistema
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..models import User, BotConfiguration
from ..auth import get_current_user

router = APIRouter(prefix="/api/admin/bots", tags=["admin-bots"])

@router.get("/all")
def get_all_bots(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar TODOS os bots do sistema (admin only)"""
    
    # Verificar se é admin
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Apenas admins")
    
    # Buscar TODOS os bots com join no user
    bots = db.query(BotConfiguration).join(User).all()
    
    result = []
    for bot in bots:
        user = db.query(User).filter(User.id == bot.user_id).first()
        
        result.append({
            "id": bot.id,
            "name": bot.name,
            "exchange": bot.exchange,
            "symbols": bot.symbols if isinstance(bot.symbols, list) else [bot.symbols],
            "strategy": bot.strategy,
            "capital": float(bot.capital) if bot.capital else 0,
            "is_active": bot.is_active,
            "user_id": bot.user_id,
            "user_email": user.email if user else "N/A",
            "user_name": f"{user.first_name} {user.last_name}" if user else "N/A",
            "created_at": bot.created_at.isoformat() if bot.created_at else None
        })
    
    print(f"[Admin Bots] Retornando {len(result)} bots do sistema")
    
    return {"bots": result, "total": len(result)}

@router.get("/count")
def count_bots(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Contar bots (admin)"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Apenas admins")
    
    total = db.query(BotConfiguration).count()
    ativos = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).count()
    
    return {"total": total, "active": ativos}

