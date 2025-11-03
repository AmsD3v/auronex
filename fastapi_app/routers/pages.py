"""
Router para Páginas HTML - Frontend do RoboTrader
Landing Page, Dashboard, Cadastro, Pagamento, etc.
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..auth import get_password_hash, verify_password, create_access_token
from ..utils.auth_pages import require_auth, require_admin, get_user_plan, get_current_user_from_cookie, get_payment_status

# Configurar templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(tags=["páginas-html"])

# ========================================
# LANDING PAGE
# ========================================

@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request, db: Session = Depends(get_db)):
    """Landing Page principal - Home"""
    user = get_current_user_from_cookie(request, db)
    plan = get_user_plan(request, db) if user else "guest"
    
    return templates.TemplateResponse("landing.html", {
        "request": request,
        "title": "RoboTrader - Bot de Trading Automatizado",
        "user": user,
        "plan": plan
    })

# ========================================
# AUTENTICAÇÃO - PÁGINAS
# ========================================

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de cadastro"""
    return templates.TemplateResponse("register.html", {
        "request": request,
        "title": "Criar Conta - RoboTrader"
    })

@router.post("/register", response_class=HTMLResponse)
async def register_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(default=""),
    first_name: str = Form(...),
    last_name: str = Form(...),
    cpf: str = Form(default=""),
    celular: str = Form(default=""),
    db: Session = Depends(get_db)
):
    """Processar cadastro"""
    
    # Validar senhas conferem
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "title": "Criar Conta - RoboTrader",
            "error": "As senhas não conferem!"
        })
    
    # Remover formatação do CPF
    cpf_numbers = ''.join(filter(str.isdigit, cpf))
    
    # Validar CPF
    if len(cpf_numbers) != 11:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "title": "Criar Conta - RoboTrader",
            "error": "CPF inválido! Deve ter 11 dígitos."
        })
    
    # Verificar se email já existe
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "title": "Criar Conta - RoboTrader",
            "error": "Este email já está cadastrado!"
        })
    
    # Verificar se CPF já existe
    existing_cpf = db.query(User).filter(User.cpf == cpf_numbers).first()
    if existing_cpf:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "title": "Criar Conta - RoboTrader",
            "error": "Este CPF já está cadastrado! Apenas um cadastro por CPF."
        })
    
    # Criar usuário (SIMPLIFICADO - sem erros!)
    try:
        from datetime import datetime
        
        user = User(
            username=email.split('@')[0],
            email=email,
            password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            cpf=cpf_numbers,
            celular=celular,
            is_active=True,
            is_staff=False,
            is_superuser=False,
            date_joined=datetime.utcnow()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Criar token JWT
        access_token = create_access_token(data={"user_id": user.id, "email": user.email})
        
        # Criar assinatura FREE (em transação separada)
        try:
            from ..models_payment import Subscription
            
            # Limpar estado da sessão primeiro
            db.rollback()
            
            subscription_free = Subscription(
                user_id=user.id,
                plan="free",
                status="active",
                payment_method="none",
                amount=0,
                currency="BRL"
            )
            db.add(subscription_free)
            db.commit()
        except Exception as e:
            print(f"Info: Subscription não criada: {e}")
            db.rollback()  # Limpar erro
        
        # FLUXO CORRETO: LOGAR O USUÁRIO IMEDIATAMENTE!
        # Criar token JWT
        access_token = create_access_token(data={"user_id": user.id, "email": user.email})
        
        print(f"✅ Cadastro: Token criado para {user.email}")
        
        # Redirecionar para escolha de plano (JÁ LOGADO!)
        response = RedirectResponse(url="/payment/choice", status_code=303)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=False,  # JavaScript precisa ler!
            max_age=86400,
            samesite="lax"
        )
        
        print(f"✅ Cadastro: Cookie setado!")
        
        return response
        
    except Exception as e:
        db.rollback()
        # Mostrar erro específico para debug
        return templates.TemplateResponse("register.html", {
            "request": request,
            "title": "Criar Conta - RoboTrader",
            "error": f"Erro ao processar cadastro. Detalhes: {str(e)[:200]}"
        })

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, registered: bool = False, reset: str = "", next: str = "/dashboard"):
    """Página de login"""
    
    message = None
    if registered:
        message = "Conta criada com sucesso! Faça login."
    elif reset == "success":
        message = "Senha redefinida com sucesso! Faça login com a nova senha."
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login - Auronex",
        "success_message": message,
        "next": next
    })

@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Página de recuperação de senha"""
    return templates.TemplateResponse("forgot_password.html", {
        "request": request,
        "title": "Recuperar Senha - Auronex"
    })

@router.post("/forgot-password", response_class=HTMLResponse)
async def forgot_password_submit(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    """Processar recuperação de senha - COMPLETO E FUNCIONAL"""
    
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Criar token de reset
        from ..models_password_reset import PasswordResetToken
        from ..utils.email_sender import generate_reset_token, send_password_reset_email
        from datetime import datetime, timedelta
        
        # Gerar token seguro
        token = generate_reset_token()
        expires = datetime.utcnow() + timedelta(hours=1)
        
        # Salvar no banco
        reset_token = PasswordResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires
        )
        
        db.add(reset_token)
        db.commit()
        
        # Criar link de reset
        reset_link = f"http://localhost:8001/reset-password/{token}"
        
        # Enviar email (simulação em localhost)
        send_password_reset_email(user.email, reset_link)
        
        return templates.TemplateResponse("forgot_password.html", {
            "request": request,
            "title": "Recuperar Senha - Auronex",
            "success": True,
            "reset_link": reset_link  # Mostrar link (só em desenvolvimento!)
        })
    else:
        return templates.TemplateResponse("forgot_password.html", {
            "request": request,
            "title": "Recuperar Senha - Auronex",
            "error": "Email não encontrado."
        })

@router.get("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_page(request: Request, token: str, db: Session = Depends(get_db)):
    """Página para redefinir senha com token"""
    
    from ..models_password_reset import PasswordResetToken
    
    # Verificar token
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()
    
    if not reset_token or not reset_token.is_valid():
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "title": "Link Inválido - Auronex",
            "error": "Link de recuperação inválido ou expirado."
        })
    
    return templates.TemplateResponse("reset_password.html", {
        "request": request,
        "title": "Redefinir Senha - Auronex",
        "token": token
    })

@router.post("/reset-password/{token}", response_class=HTMLResponse)
async def reset_password_submit(
    request: Request,
    token: str,
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Processar redefinição de senha"""
    
    from ..models_password_reset import PasswordResetToken
    
    # Validar senhas
    if new_password != confirm_password:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "title": "Redefinir Senha - Auronex",
            "token": token,
            "error": "As senhas não conferem!"
        })
    
    if len(new_password) < 6:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "title": "Redefinir Senha - Auronex",
            "token": token,
            "error": "Senha deve ter no mínimo 6 caracteres!"
        })
    
    # Verificar token
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()
    
    if not reset_token or not reset_token.is_valid():
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "title": "Link Inválido - Auronex",
            "error": "Link de recuperação inválido ou expirado."
        })
    
    # Buscar usuário
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    
    if not user:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "title": "Erro - Auronex",
            "error": "Usuário não encontrado."
        })
    
    # Atualizar senha
    user.password = get_password_hash(new_password)
    
    # Marcar token como usado
    reset_token.used = True
    
    db.commit()
    
    # Redirecionar para login com mensagem
    return RedirectResponse(url="/login?reset=success", status_code=303)

@router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Processar login"""
    
    # Buscar usuário
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Login - Auronex",
            "error": "Email ou senha incorretos!"
        })
    
    # Criar token
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    
    print(f"✅ Token criado para {user.email}: {access_token[:30]}...")
    
    # Determinar para onde redirecionar
    redirect_url = "/dashboard"
    
    # Pegar 'next' do form (se existir)
    form_data = await request.form()
    next_url = form_data.get("next", "")
    
    if next_url and next_url != "/dashboard":
        redirect_url = next_url
    elif user.is_staff or user.is_superuser:
        redirect_url = "/admin/"
    
    print(f"✅ Redirecionando para: {redirect_url}")
    
    response = RedirectResponse(url=redirect_url, status_code=303)
    
    # CRÍTICO: Setar cookie SEM httponly para JavaScript acessar!
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=False,  # ← MUDANÇA CRÍTICA! JS precisa ler
        max_age=86400,
        samesite="lax"
    )
    
    print(f"✅ Cookie access_token setado!")
    
    return response

# ========================================
# DASHBOARD DO USUÁRIO
# ========================================

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    """Dashboard do usuário - PROTEGIDO"""
    user = require_auth(request, db)
    
    # Se não logado, redirecionar
    if not user:
        return RedirectResponse(url="/login?next=/dashboard", status_code=303)
    
    plan = get_user_plan(request, db)
    payment_status = get_payment_status(request, db)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "Dashboard - RoboTrader",
        "user": user,
        "plan": plan,
        "payment_status": payment_status
    })

# ========================================
# CONFIGURAÇÕES
# ========================================

@router.get("/api-keys-page", response_class=HTMLResponse)
async def api_keys_page(request: Request, db: Session = Depends(get_db)):
    """Página de gerenciamento de API Keys - PROTEGIDA"""
    user = require_auth(request, db)
    
    if not user:
        return RedirectResponse(url="/login?next=/api-keys-page", status_code=303)
    
    plan = get_user_plan(request, db)
    
    return templates.TemplateResponse("api_keys.html", {
        "request": request,
        "title": "API Keys - RoboTrader",
        "user": user,
        "plan": plan
    })

@router.get("/bots-page", response_class=HTMLResponse)
async def bots_page(request: Request, db: Session = Depends(get_db)):
    """Página de configuração de bots - PROTEGIDA"""
    user = require_auth(request, db)
    
    if not user:
        return RedirectResponse(url="/login?next=/bots-page", status_code=303)
    
    plan = get_user_plan(request, db)
    
    return templates.TemplateResponse("bots.html", {
        "request": request,
        "title": "Meus Bots - RoboTrader",
        "user": user,
        "plan": plan
    })

# ========================================
# PAGAMENTOS
# ========================================

@router.get("/pricing", response_class=HTMLResponse)
async def pricing_page(request: Request, db: Session = Depends(get_db)):
    """Página de planos e preços - Lógica de upgrade"""
    user = get_current_user_from_cookie(request, db)
    user_plan = get_user_plan(request, db)
    
    # Planos disponíveis baseado no plano atual (SEM DOWNGRADE!)
    available_plans = []
    
    if user_plan == "guest":
        available_plans = ["free", "pro", "premium"]  # Visitante vê todos
    elif user_plan == "free":
        available_plans = ["pro", "premium"]  # FREE: Esconde Free, mostra Pro e Premium
    elif user_plan == "pro":
        available_plans = ["premium"]  # PRO: Esconde Free e Pro, mostra apenas Premium
    elif user_plan == "premium":
        available_plans = []  # PREMIUM: Nenhum upgrade (formulário contato)
    
    # Texto do título
    page_title = "Upgrade Seu Plano" if user else "Escolha Seu Plano"
    
    return templates.TemplateResponse("pricing.html", {
        "request": request,
        "title": "Planos e Preços - RoboTrader",
        "user": user,
        "plan": user_plan,
        "available_plans": available_plans,
        "page_title": page_title
    })

@router.get("/payment/choice", response_class=HTMLResponse)
async def payment_choice_page(request: Request, db: Session = Depends(get_db)):
    """Escolha de plano PÓS-CADASTRO - USUÁRIO JÁ ESTÁ LOGADO"""
    
    # Usuário DEVE estar logado aqui
    user = get_current_user_from_cookie(request, db)
    
    # Se não está logado, redireciona para cadastro
    if not user:
        return RedirectResponse(url="/register", status_code=303)
    
    return templates.TemplateResponse("payment_choice.html", {
        "request": request,
        "title": "Escolha Seu Plano - RoboTrader",
        "user": user
    })

@router.get("/payment/confirm-free", response_class=HTMLResponse)
async def confirm_free_plan(request: Request, db: Session = Depends(get_db)):
    """Confirmar plano FREE - usuário já está logado"""
    
    # Usuário JÁ está logado (login foi feito no cadastro)
    user = get_current_user_from_cookie(request, db)
    
    if not user:
        return RedirectResponse(url="/register", status_code=303)
    
    # Apenas redirecionar para dashboard (já está logado!)
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/payment/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request, plan: str = "pro", db: Session = Depends(get_db)):
    """Página de checkout - USUÁRIO DEVE ESTAR LOGADO!"""
    
    # CRÍTICO: Verificar se está logado!
    user = get_current_user_from_cookie(request, db)
    
    if not user:
        # Se não está logado, redireciona para login
        return RedirectResponse(url=f"/login?next=/payment/checkout?plan={plan}", status_code=303)
    
    plans = {
        "free": {"name": "Free", "price": 0},
        "pro": {"name": "Pro", "price": 29.90},
        "premium": {"name": "Premium", "price": 99.90}
    }
    
    selected_plan = plans.get(plan, plans["pro"])
    
    return templates.TemplateResponse("checkout.html", {
        "request": request,
        "title": "Checkout - Auronex Robô Trader",
        "plan": selected_plan,
        "plan_id": plan,
        "user": user  # Passar usuário para template
    })

# ========================================
# ADMIN (futuro)
# ========================================

@router.get("/admin/", response_class=HTMLResponse)  # URL ÚNICA
@router.get("/admin", response_class=HTMLResponse)  # Redirect automático
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    """Painel administrativo - APENAS ADMINS"""
    user = require_auth(request, db)
    
    if not user:
        return RedirectResponse(url="/login?next=/admin", status_code=303)
    
    # Verificar se é admin
    if not user.is_staff and not user.is_superuser:
        return templates.TemplateResponse("error_403.html", {
            "request": request,
            "title": "Acesso Negado",
            "error": "Apenas administradores podem acessar esta página."
        })
    
    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "title": "Painel Admin - RoboTrader",
        "user": user
    })

# ========================================
# OUTRAS PÁGINAS
# ========================================

@router.get("/docs-page", response_class=HTMLResponse)
async def docs_page(request: Request, db: Session = Depends(get_db)):
    """Documentação do sistema"""
    user = get_current_user_from_cookie(request, db)
    plan = get_user_plan(request, db)
    
    return templates.TemplateResponse("docs.html", {
        "request": request,
        "title": "Documentação - Auronex",
        "user": user,
        "plan": plan
    })

@router.get("/terms", response_class=HTMLResponse)
async def terms_page(request: Request):
    """Termos de Uso"""
    return templates.TemplateResponse("terms.html", {
        "request": request,
        "title": "Termos de Uso - Auronex"
    })

@router.get("/privacy", response_class=HTMLResponse)
async def privacy_page(request: Request):
    """Política de Privacidade"""
    return templates.TemplateResponse("privacy.html", {
        "request": request,
        "title": "Política de Privacidade - Auronex"
    })

@router.get("/payment/pix", response_class=HTMLResponse)
async def payment_pix_page(request: Request, plan: str = "pro"):
    """Página de pagamento PIX - Simulação realista"""
    
    plans = {
        "free": {"name": "Free", "price": 0},
        "pro": {"name": "Pro", "price": 29.90},
        "premium": {"name": "Premium", "price": 99.90}
    }
    
    selected_plan = plans.get(plan, plans["pro"])
    
    return templates.TemplateResponse("payment_pix.html", {
        "request": request,
        "title": "Pagamento PIX - RoboTrader",
        "plan": selected_plan
    })

@router.get("/payment/card", response_class=HTMLResponse)
async def payment_card_page(request: Request, plan: str = "pro"):
    """Página de pagamento com Cartão - Simulação realista"""
    
    plans = {
        "free": {"name": "Free", "price": 0},
        "pro": {"name": "Pro", "price": 29.90},
        "premium": {"name": "Premium", "price": 99.90}
    }
    
    selected_plan = plans.get(plan, plans["pro"])
    
    return templates.TemplateResponse("payment_card.html", {
        "request": request,
        "title": "Pagamento com Cartão - RoboTrader",
        "plan": selected_plan
    })

@router.get("/payment/success", response_class=HTMLResponse)
async def payment_success_page(request: Request, plan: str = "pro", payment_confirmed: bool = False, db: Session = Depends(get_db)):
    """Página de sucesso após pagamento - CRIAR/ATUALIZAR SUBSCRIPTION"""
    
    try:
        # CRÍTICO: Usuário DEVE estar logado para ativar o plano!
        user = get_current_user_from_cookie(request, db)
        
        if not user:
            # Se não está logado, algo deu muito errado!
            print(f"⚠️ ERRO: Usuário não está logado em /payment/success!")
            return RedirectResponse(url="/login?error=session_expired", status_code=303)
        
        print(f"✅ Usuário {user.id} ({user.email}) em /payment/success, plano: {plan}")
        
        if user:
                # Criar token
                access_token = create_access_token(data={"user_id": user.id, "email": user.email})
                
                # Criar/Atualizar assinatura do plano pago
                try:
                    from ..models_payment import Subscription
                    db.rollback()  # Limpar sessão
                    
                    # Verificar se já existe subscription
                    existing_sub = db.query(Subscription).filter(
                        Subscription.user_id == user.id
                    ).first()
                    
                    if existing_sub:
                        # Atualizar subscription existente
                        existing_sub.plan = plan
                        existing_sub.status = "active"
                        existing_sub.amount = 1.00 if plan == "pro" else (5.00 if plan == "premium" else 0)
                        existing_sub.currency = "BRL"
                        existing_sub.payment_method = "paid"
                        print(f"✅ Subscription atualizada: User {user.id} ({user.email}) → Plano {plan}")
                    else:
                        # Criar nova subscription
                        subscription = Subscription(
                            user_id=user.id,
                            plan=plan,
                            status="active",
                            payment_method="paid",
                            amount=1.00 if plan == "pro" else (5.00 if plan == "premium" else 0),
                            currency="BRL"
                        )
                        db.add(subscription)
                        print(f"✅ Subscription criada: User {user.id} ({user.email}) → Plano {plan}")
                    
                    db.commit()
                except Exception as e:
                    print(f"⚠ Erro ao criar subscription: {e}")
                    db.rollback()
                
                # Retornar com cookie de login
                response = templates.TemplateResponse("payment_success.html", {
                    "request": request,
                    "title": "Pagamento Aprovado!",
                    "plan": plan
                })
                
                response.set_cookie(
                    key="access_token",
                    value=f"Bearer {access_token}",
                    httponly=True,
                    max_age=86400
                )
                response.delete_cookie("pending_user_id")
                
                return response
        
        # Fallback simples
        return templates.TemplateResponse("payment_success.html", {
            "request": request,
            "title": "Pagamento Aprovado!"
        })
        
    except Exception as e:
        # Se qualquer erro, mostrar página simples
        print(f"Erro em payment_success: {e}")
        return templates.TemplateResponse("payment_success.html", {
            "request": request,
            "title": "Pagamento Aprovado!"
        })

@router.get("/payment/cancelled", response_class=HTMLResponse)
async def payment_cancelled_page(request: Request):
    """Página quando pagamento é cancelado"""
    return templates.TemplateResponse("payment_cancelled.html", {
        "request": request,
        "title": "Pagamento Cancelado - RoboTrader"
    })

@router.get("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    """Logout do usuário - Inteligente (admin → login, user → home)"""
    
    # Verificar se era admin
    user = get_current_user_from_cookie(request, db)
    
    # Se era admin, volta para login do admin
    if user and (user.is_staff or user.is_superuser):
        response = RedirectResponse(url="/login?next=/admin/", status_code=303)
    else:
        # Usuário comum vai para landing page
        response = RedirectResponse(url="/", status_code=303)
    
    response.delete_cookie("access_token")
    return response

