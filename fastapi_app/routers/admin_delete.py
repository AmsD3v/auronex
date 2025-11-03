"""
API para deletar usuário completo
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, BotConfiguration, ExchangeAPIKey
from ..models_payment import Subscription, Payment

router = APIRouter(prefix="/api/admin", tags=["admin-delete"])

@router.delete("/users/{user_id}/delete-complete")
async def delete_user_complete(user_id: int, db: Session = Depends(get_db)):
    """Deletar usuário e TODOS os seus dados"""
    
    try:
        # Buscar usuário
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Deletar bots
        db.query(BotConfiguration).filter(BotConfiguration.user_id == user_id).delete()
        
        # Deletar API keys
        db.query(ExchangeAPIKey).filter(ExchangeAPIKey.user_id == user_id).delete()
        
        # Deletar subscriptions
        db.query(Subscription).filter(Subscription.user_id == user_id).delete()
        
        # Deletar payments
        db.query(Payment).filter(Payment.user_id == user_id).delete()
        
        # Deletar usuário
        db.delete(user)
        
        db.commit()
        
        return {"success": True, "message": f"Usuário {user.email} e todos os dados deletados"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



