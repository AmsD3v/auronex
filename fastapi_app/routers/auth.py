"""
Router de Autenticação - Login/Register
✅ Com Rate Limiting e Validações
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserRegister, UserLogin, Token, UserResponse
from ..auth import get_password_hash, verify_password, create_access_token, create_refresh_token, verify_refresh_token, get_current_user
from ..validators import validate_password_strength, validate_email, sanitize_string
from ..rate_limiter import rate_limiter

router = APIRouter(prefix="/api/auth", tags=["autenticação"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Criar nova conta com validação de senha forte"""
    
    # ✅ Validar formato de email
    is_valid_email, email_message = validate_email(user_data.email)
    if not is_valid_email:
        raise HTTPException(
            status_code=400,
            detail=email_message
        )
    
    # ✅ Validar força da senha
    is_valid_password, password_message = validate_password_strength(user_data.password)
    if not is_valid_password:
        raise HTTPException(
            status_code=400,
            detail=password_message
        )
    
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

@router.post("/login")
async def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login e obter token JWT + user data
    ✅ Rate Limiting: 5 tentativas por minuto por IP
    """
    
    # ✅ RATE LIMITING - Prevenir brute force
    client_ip = request.client.host
    allowed, remaining = rate_limiter.check_rate_limit_ip(
        ip=client_ip,
        max_requests=5,  # 5 tentativas
        window_seconds=60  # por minuto
    )
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Muitas tentativas de login. Aguarde 1 minuto e tente novamente.",
            headers={"Retry-After": "60"}
        )
    
    # ✅ DEBUG: Log detalhado do login
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"[LOGIN] Tentativa de login: {credentials.email}")
    
    # Buscar usuário
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user:
        logger.warning(f"[LOGIN] Usuário NÃO encontrado: {credentials.email}")
        raise HTTPException(
            status_code=401,
            detail="Email ou senha incorretos"
        )
    
    logger.info(f"[LOGIN] Usuário encontrado: ID={user.id}, Email={user.email}")
    logger.info(f"[LOGIN] Hash no banco começa com: {user.password[:20]}...")
    
    # Verificar senha
    try:
        senha_correta = verify_password(credentials.password, user.password)
        logger.info(f"[LOGIN] Verificação senha: {'OK' if senha_correta else 'FALHOU'}")
        
        if not senha_correta:
            logger.warning(f"[LOGIN] Senha INCORRETA para {credentials.email}")
            raise HTTPException(
                status_code=401,
                detail="Email ou senha incorretos"
            )
    except Exception as e:
        logger.error(f"[LOGIN] ERRO ao verificar senha: {e}")
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
    
    # ✅ Criar AMBOS os tokens
    token_data = {"user_id": user.id, "email": user.email}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    # ✅ Retornar USER com dados completos + AMBOS tokens
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,  # ✅ Token separado para refresh
        "token_type": "bearer",
        "expires_in": 15 * 60,  # 15 minutos em segundos
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name or user.email.split('@')[0],
            "last_name": user.last_name or "",
            "is_active": user.is_active,
            "subscription": None
        }
    }

@router.post("/refresh")
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Renovar Access Token usando Refresh Token
    
    Body:
        {
            "refresh_token": "eyJ..."
        }
    
    Returns:
        Novo access_token (refresh_token continua o mesmo)
    """
    # ✅ Verificar refresh token
    payload = verify_refresh_token(refresh_token)
    
    user_id = payload.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    # Verificar se usuário ainda existe e está ativo
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # ✅ Gerar NOVO access token
    new_access_token = create_access_token(
        data={"user_id": user.id, "email": user.email}
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": 15 * 60  # 15 minutos
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Obter usuário atual com dados completos"""
    # ✅ Se first_name vazio, usar email
    if not current_user.first_name or current_user.first_name.strip() == '':
        current_user.first_name = current_user.email.split('@')[0]
    
    return current_user

