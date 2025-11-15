"""
Autenticação JWT - FastAPI
✅ Com Refresh Token e expiração curta
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

# ✅ CARREGAR .env PRIMEIRO!
load_dotenv()

from .database import get_db
from .models import User

# ✅ SEGURANÇA: Carregar do .env
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY não configurada! "
        "Gere com: openssl rand -hex 32"
    )

ALGORITHM = os.getenv('ALGORITHM', 'HS256')

# ✅ Tokens - DESENVOLVIMENTO = longo, PRODUÇÃO = curto
if os.getenv('ENVIRONMENT') == 'production':
    ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Produção: 15 min
else:
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # Desenvolvimento: 24 horas
    
REFRESH_TOKEN_EXPIRE_DAYS = 7  # 7 dias

# Password hashing (Django + bcrypt + argon2 - compatibilidade TOTAL)
# ✅ CRÍTICO: Aceita senhas Django (pbkdf2), bcrypt E argon2
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt", "argon2"],  # ✅ Aceita TODOS
    deprecated="auto"  # Migra automaticamente
)

# Security scheme
security = HTTPBearer()

def verify_password(plain_password, hashed_password):
    """Verificar senha"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash da senha"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Criar Access Token (curta duração)
    
    Args:
        data: Dados para incluir no token (ex: user_id)
        expires_delta: Tempo de expiração customizado
    
    Returns:
        Token JWT assinado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "type": "access"  # ✅ Tipo do token
    })
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    """
    Criar Refresh Token (longa duração)
    
    Args:
        data: Dados para incluir no token (ex: user_id)
    
    Returns:
        Refresh token JWT assinado
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "type": "refresh"  # ✅ Tipo do token
    })
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_refresh_token(refresh_token: str) -> dict:
    """
    Verificar Refresh Token
    
    Args:
        refresh_token: Token a verificar
    
    Returns:
        Payload do token
    
    Raises:
        HTTPException: Se token inválido
    """
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # ✅ Verificar tipo do token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido (não é refresh token)"
            )
        
        return payload
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obter usuário atual do Access Token
    
    Args:
        credentials: Credenciais Bearer token
        db: Sessão do banco
    
    Returns:
        Usuário autenticado
    
    Raises:
        HTTPException: Se token inválido
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # ✅ Verificar tipo do token
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido (use access token)"
            )
        
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Usuário inativo"
        )
    
    return user


