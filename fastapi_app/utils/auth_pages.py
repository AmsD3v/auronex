"""
Autenticação para Páginas HTML
Middleware e helpers para proteger rotas
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..auth import SECRET_KEY, ALGORITHM

def get_current_user_from_cookie(request: Request, db: Session) -> User:
    """
    Obter usuário do cookie de autenticação
    Usado em páginas HTML
    """
    
    # DEBUG
    print(f"[AUTH] Verificando autenticacao...")
    print(f"[AUTH] Cookies disponiveis: {list(request.cookies.keys())}")
    
    # Pegar token do cookie
    token = request.cookies.get("access_token")
    
    if token:
        print(f"[AUTH] Token encontrado: {token[:50]}...")
    else:
        print("[AUTH] Nenhum token no cookie!")
        return None
    
    # Remover "Bearer " se existir
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
        print("[AUTH] Removido prefixo Bearer")
    
    try:
        # Decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        
        print(f"[AUTH] Token valido! user_id: {user_id}")
        
        if user_id is None:
            print("[AUTH] ERRO: user_id None no payload!")
            return None
        
        # Buscar usuário no banco
        user = db.query(User).filter(User.id == user_id).first()
        
        if user:
            print(f"[AUTH] Usuario autenticado: {user.email}")
        else:
            print(f"[AUTH] ERRO: Usuario {user_id} nao encontrado!")
        
        return user
        
    except JWTError as e:
        print(f"[AUTH] ERRO JWT: {e}")
        return None

def require_auth(request: Request, db: Session):
    """
    Verificar se usuário está autenticado
    Se não estiver, redireciona para login
    
    IMPORTANTE: Esta função retorna None se não autenticado
    A rota deve verificar e fazer redirect manualmente
    """
    
    user = get_current_user_from_cookie(request, db)
    return user  # Retorna None se não autenticado

def require_admin(request: Request, db: Session):
    """
    Verificar se usuário é admin/staff
    """
    
    user = require_auth(request, db)
    
    if not user.is_staff and not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores."
        )
    
    return user

def get_user_plan(request: Request, db: Session):
    """
    Obter plano atual do usuário (free, pro, premium)
    """
    
    user = get_current_user_from_cookie(request, db)
    
    if not user:
        return "guest"  # Visitante não logado
    
    # Buscar assinatura ativa
    try:
        from ..models_payment import Subscription
        
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.status == "active"
        ).order_by(Subscription.id.desc()).first()
        
        if not subscription:
            return "free"  # Usuário sem assinatura = free
        
        return subscription.plan  # free, pro, premium
    except:
        # Se tabela não existe ou erro, retorna free
        return "free"

def get_payment_status(request: Request, db: Session):
    """
    Verificar se usuário tem pagamento pendente
    Retorna: 'active', 'pending', ou 'none'
    """
    
    user = get_current_user_from_cookie(request, db)
    
    if not user:
        return "none"
    
    try:
        from ..models_payment import Subscription
        
        subscription = db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.status == "active"
        ).order_by(Subscription.id.desc()).first()
        
        if not subscription:
            return "none"  # Sem subscription
        
        # Se plano é FREE, está OK
        if subscription.plan == "free":
            return "active"
        
        # Se plano é PRO/PREMIUM e payment_method está vazio ou é 'none'
        if subscription.payment_method in [None, "none", "simulated"]:
            return "pending"  # Escolheu plano mas não pagou
        
        return "active"  # Tudo OK
        
    except:
        return "none"

