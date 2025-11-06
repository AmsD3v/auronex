"""
Endpoints PÚBLICOS de Pagamento
Não exigem autenticação JWT - aceitam pending_user_id
PARA PRODUÇÃO - PAGAMENTOS REAIS
"""

from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from decimal import Decimal
from datetime import datetime, timedelta

from ..database import get_db
from ..models import User
from ..models_payment import Subscription, Payment

router = APIRouter(prefix="/api/payments-public", tags=["pagamentos-publicos"])

# Chaves de PRODUÇÃO
MERCADOPAGO_ACCESS_TOKEN = "APP_USR-7940373206085562-102818-e0b751adbf15c2d81e094a3dc01b0cef-2953317711"
STRIPE_SECRET_KEY = "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"

# Planos (VALORES REAIS DE PRODUÇÃO!) - ATUALIZADOS 06/11/2025
PLANS = {
    "pro": {"name": "Pro", "price": 29.90, "currency": "BRL", "bots_limit": 3, "cryptos_limit": 2},  # ✅ Mantém R$ 29,90
    "premium": {"name": "Premium", "price": 59.90, "currency": "BRL", "bots_limit": 5, "cryptos_limit": 3}  # ✅ R$ 59,90 (era 99,90)
}

@router.post("/mercadopago/checkout")
async def create_mercadopago_checkout_public(request: Request, db: Session = Depends(get_db)):
    """Criar Checkout Pro do MercadoPago - PIX + Cartão + Boleto - PRODUÇÃO"""
    
    try:
        body = await request.json()
        plan = body.get("plan", "pro")
        
        # Pegar usuário LOGADO
        from ..utils.auth_pages import get_current_user_from_cookie
        user = get_current_user_from_cookie(request, db)
        
        if not user:
            raise HTTPException(status_code=401, detail="Faça login para continuar")
        
        # Configurações do plano
        plan_config = PLANS.get(plan, PLANS["pro"])
        
        # Criar Checkout Pro do MercadoPago (PIX + Cartão + Boleto)
        import mercadopago
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        
        # Dados da preferência (SEM auto_return para funcionar com localhost)
        preference_data = {
            "items": [
                {
                    "title": f"RoboTrader {plan_config['name']}",
                    "quantity": 1,
                    "unit_price": float(plan_config["price"])
                }
            ],
            "payer": {
                "name": user.first_name,
                "surname": user.last_name,
                "email": user.email
            },
            "back_urls": {
                "success": f"https://auronex.com.br/payment/success?plan={plan}",
                "failure": f"https://auronex.com.br/payment/cancelled?plan={plan}",
                "pending": f"https://auronex.com.br/payment/success?plan={plan}"
            },
            "external_reference": f"user_{user.id}_plan_{plan}"
            # Sem auto_return (localhost não suporta)
        }
        
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        
        # Retornar URL do Checkout Pro (redireciona para página do MercadoPago)
        return {
            "success": True,
            "checkout_url": preference.get("init_point"),  # URL para navegador
            "sandbox_url": preference.get("sandbox_init_point"),  # URL teste
            "preference_id": preference.get("id"),
            "amount": plan_config["price"]
        }
        
    except ImportError:
        raise HTTPException(status_code=500, detail="MercadoPago SDK não instalado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar PIX: {str(e)}")


@router.post("/stripe/checkout")
async def create_stripe_checkout_public(request: Request, db: Session = Depends(get_db)):
    """Criar checkout Stripe - PRODUÇÃO - Aceita pending_user_id"""
    
    try:
        body = await request.json()
        plan = body.get("plan", "pro")
        
        # Pegar usuário LOGADO
        from ..utils.auth_pages import get_current_user_from_cookie
        user = get_current_user_from_cookie(request, db)
        
        if not user:
            raise HTTPException(status_code=401, detail="Faça login para continuar")
        
        # Configurações do plano
        plan_config = PLANS.get(plan, PLANS["pro"])
        
        # Criar checkout Stripe REAL
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        
        checkout_session = stripe.checkout.Session.create(
            customer_email=user.email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'brl',
                    'unit_amount': int(plan_config["price"] * 100),  # Centavos
                    'product_data': {
                        'name': f'RoboTrader - Plano {plan_config["name"]}',
                        'description': 'Bot de Trading Automatizado',
                    },
                    'recurring': {
                        'interval': 'month'
                    }
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f'https://auronex.com.br/payment/success?plan={plan}&session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url='https://auronex.com.br/payment/cancelled',
            metadata={
                'user_id': user.id,
                'plan': plan
            }
        )
        
        # Tentar salvar no banco (não bloquear se falhar)
        try:
            db.rollback()  # Limpar sessão
            
            db_payment = Payment(
                user_id=user.id,
                amount=Decimal(str(plan_config["price"])),
                currency="BRL",
                status="pending",
                gateway="stripe",
                gateway_payment_id=checkout_session.id
            )
            
            db.add(db_payment)
            db.commit()
        except Exception as e:
            print(f"Info: Não salvou no banco: {e}")
            db.rollback()
        
        # Retornar URL do checkout Stripe REAL
        return {
            "success": True,
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id
        }
        
    except ImportError:
        raise HTTPException(status_code=500, detail="Stripe SDK não instalado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar checkout: {str(e)}")

