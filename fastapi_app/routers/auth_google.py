"""
Google OAuth Login
Permite login com conta Google
"""

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

from ..database import get_db
from ..models import User
from ..auth import create_access_token, get_password_hash
from datetime import datetime

router = APIRouter(prefix="/auth/google", tags=["google-oauth"])

# Configuração OAuth (use variáveis de ambiente em produção!)
config = Config(environ={
    'GOOGLE_CLIENT_ID': '***-***.apps.googleusercontent.com',  # Substitua
    'GOOGLE_CLIENT_SECRET': '***',  # Substitua
})

oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/login")
async def google_login(request: Request):
    """Iniciar login com Google"""
    redirect_uri = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Callback do Google após autenticação"""
    
    try:
        # Obter token do Google
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            return RedirectResponse(url="/login?error=google_failed", status_code=303)
        
        # Dados do Google
        google_email = user_info.get('email')
        google_name = user_info.get('name', '').split(' ')
        first_name = google_name[0] if google_name else 'Usuário'
        last_name = ' '.join(google_name[1:]) if len(google_name) > 1 else 'Google'
        
        # Verificar se usuário já existe
        existing_user = db.query(User).filter(User.email == google_email).first()
        
        if existing_user:
            # Login existente
            access_token = create_access_token(data={"user_id": existing_user.id, "email": existing_user.email})
            
            response = RedirectResponse(url="/dashboard", status_code=303)
            response.set_cookie(
                key="access_token",
                value=f"Bearer {access_token}",
                httponly=True,
                max_age=86400
            )
            
            return response
        else:
            # Criar novo usuário
            new_user = User(
                username=google_email.split('@')[0],
                email=google_email,
                password=get_password_hash('google_oauth_' + google_email),  # Senha aleatória
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_staff=False,
                is_superuser=False,
                date_joined=datetime.utcnow()
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Criar subscription FREE automática
            from ..models_payment import Subscription
            subscription_free = Subscription(
                user_id=new_user.id,
                plan="free",
                status="active",
                payment_method="none",
                amount=0,
                currency="BRL"
            )
            db.add(subscription_free)
            db.commit()
            
            # Login automático e redirecionar para completar dados (CPF, Celular)
            access_token = create_access_token(data={"user_id": new_user.id, "email": new_user.email})
            
            response = RedirectResponse(url="/complete-profile", status_code=303)
            response.set_cookie(
                key="access_token",
                value=f"Bearer {access_token}",
                httponly=True,
                max_age=86400
            )
            
            return response
            
    except Exception as e:
        print(f"Erro no Google OAuth: {e}")
        return RedirectResponse(url="/login?error=google_error", status_code=303)





