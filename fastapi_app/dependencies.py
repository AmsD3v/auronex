"""
Dependencies opcionais para FastAPI
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from .database import get_db
from .models import User
from .auth import get_current_user

# Security scheme opcional
security = HTTPBearer(auto_error=False)

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Obter usuário atual do token JWT (OPCIONAL)
    
    Se token presente: retorna usuário
    Se token ausente: retorna None
    
    Útil para endpoints que funcionam com OU sem autenticação
    """
    
    if not credentials:
        return None
    
    try:
        # Reusar lógica do get_current_user
        from .auth import SECRET_KEY, ALGORITHM
        from jose import jwt, JWTError
        
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Verificar tipo do token
        if payload.get("type") != "access":
            return None
        
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None or not user.is_active:
            return None
        
        return user
        
    except (JWTError, Exception):
        return None




