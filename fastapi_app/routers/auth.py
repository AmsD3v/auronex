"""
Router de Autenticação - Login/Register
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserRegister, UserLogin, Token, UserResponse
from ..auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["autenticação"])

@router.post("/register/", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Criar nova conta"""
    
    # Verificar se email já existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )
    
    # Criar usuário
    user = User(
        username=user_data.email.split('@')[0],  # Username = parte antes do @
        email=user_data.email,
        password=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login/", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login e obter token JWT"""
    
    # Buscar usuário
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )
    
    # Verificar senha
    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )
    
    # Verificar se está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Usuário inativo"
        )
    
    # Criar token
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    
    # ✅ Retornar USER também (Dashboard precisa!)
    return {
        "access_token": access_token,
        "refresh_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "is_active": user.is_active,
            "subscription": None  # TODO: Buscar subscription
        }
    }

@router.get("/me/", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Obter usuário atual"""
    return current_user

