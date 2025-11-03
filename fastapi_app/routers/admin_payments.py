"""
API para listar pagamentos no admin
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..models_payment import Payment

router = APIRouter(prefix="/api/admin", tags=["admin-payments"])

@router.get("/payments/")
async def list_payments(db: Session = Depends(get_db)):
    """Listar todos os pagamentos do sistema"""
    
    try:
        payments = db.query(Payment).order_by(Payment.created_at.desc()).limit(50).all()
        
        result = []
        for payment in payments:
            user = db.query(User).filter(User.id == payment.user_id).first()
            
            result.append({
                "id": payment.id,
                "user_id": payment.user_id,
                "user_email": user.email if user else None,
                "amount": float(payment.amount) if payment.amount else 0,
                "currency": payment.currency,
                "gateway": payment.gateway,
                "status": payment.status,
                "created_at": payment.created_at.isoformat() if payment.created_at else None
            })
        
        return result
        
    except Exception as e:
        print(f"Erro ao listar pagamentos: {e}")
        return []




