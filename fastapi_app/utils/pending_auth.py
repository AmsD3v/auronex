"""
Autenticação para usuários pendentes (recém-cadastrados)
Permite processar pagamento sem login completo
"""

from fastapi import Request, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User

def get_pending_user(request: Request, db: Session):
    """
    Obter usuário do pending_user_id (recém-cadastrado)
    Permite processar pagamento antes de logar
    """
    
    # Primeiro tentar pegar de pending_user_id
    pending_user_id = request.cookies.get("pending_user_id")
    
    if pending_user_id:
        try:
            user = db.query(User).filter(User.id == int(pending_user_id)).first()
            if user:
                return user
        except:
            pass
    
    # Se não tem pending, tentar JWT normal
    from .auth_pages import get_current_user_from_cookie
    user = get_current_user_from_cookie(request, db)
    
    return user











