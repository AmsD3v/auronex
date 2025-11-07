"""
Autenticação JWT - FastAPI
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

# Configurações
SECRET_KEY = "robotrader-secret-key-change-in-production-12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Password hashing (Argon2 - mais moderno e seguro que bcrypt)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Security scheme
security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    """Verificar senha"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash da senha"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Criar JWT token E registrar sessão única"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # ✅ SESSÃO - DESATIVADO temporariamente
    # if 'user_id' in data:
    #     from .middleware_session import register_session
    #     register_session(data['user_id'], encoded_jwt)
    
    return encoded_jwt

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obter usuário atual do token JWT"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    
    # ✅ SESSÃO ÚNICA - DESATIVADO temporariamente (causava problemas)
    # from .middleware_session import is_session_valid
    # if not is_session_valid(user.id, token):
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Sessão inválida. Você fez login em outro lugar.",
    #     )
    
    return user


