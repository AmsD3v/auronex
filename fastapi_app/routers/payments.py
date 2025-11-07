"""
Router de Pagamentos - MercadoPago + Stripe
Integração completa com PIX, Cartão e Assinaturas
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime, timedelta
import os

from ..database import get_db
from ..models import User
from ..models_payment import Subscription, Payment
from ..schemas_payment import PaymentCreate, PaymentResponse, SubscriptionResponse
from ..auth import get_current_user, create_access_token

router = APIRouter(prefix="/api/payments", tags=["pagamentos"])

# ========================================
# CONFIGURAÇÕES PRODUÇÃO - PAGAMENTOS REAIS! ⚠️
# ========================================

# MERCADOPAGO (Brasil - PIX + Cartão) - PRODUÇÃO
# Para PIX e Cartão, só precisa do ACCESS_TOKEN
MERCADOPAGO_ACCESS_TOKEN = "APP_USR-7940373206085562-102818-e0b751adbf15c2d81e094a3dc01b0cef-2953317711"
MERCADOPAGO_PUBLIC_KEY = "APP_USR-6ef9119a-6036-4da1-b085-c520a0d29f2d"
MERCADOPAGO_CLIENT_ID = "7940373206085562"
MERCADOPAGO_CLIENT_SECRET = "ccpL5XOYoM9AlsMeaoIpYzF6u6M1mmdl"

# STRIPE (Internacional - Cartão) - PRODUÇÃO
STRIPE_SECRET_KEY = "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"
STRIPE_PUBLISHABLE_KEY = "pk_live_51SN37vRjxbCNnFAQ14aGnoYQd5YElcrVB4hKXa98M42R0Qun9p7DN64ff2SDu0u24IJjIS06cGSYzajaeau9fpOc00JgDpcJhI"

print("[AVISO] Chaves de PRODUCAO configuradas!")
print("[AVISO] Pagamentos REAIS serao processados!")

# Planos disponíveis - VALORES REAIS ATUALIZADOS 06/11/2025
PLANS = {
    "free": {"name": "Free", "price": 0, "currency": "BRL", "bots_limit": 1, "cryptos_limit": 1, "duration": "3 dias"},  # ✅ 3 dias
    "pro": {"name": "Pro", "price": 29.90, "currency": "BRL", "bots_limit": 3, "cryptos_limit": 2, "duration": "mensal"},  # ✅ 3 bots, 2 cryptos
    "premium": {"name": "Premium", "price": 59.90, "currency": "BRL", "bots_limit": 5, "cryptos_limit": 3, "duration": "mensal"}  # ✅ 5 bots, 3 cryptos, R$ 59,90
}

# ========================================
# MERCADOPAGO - PIX + CARTÃO
# ========================================

@router.post("/mercadopago/create-payment")
async def create_mercadopago_payment(
    request: Request,
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    """Criar pagamento via MercadoPago (PIX ou Cartão) - ACEITA PENDING USER"""
    
    # Pegar usuário (pode ser pending ou logado)
    from ..utils.pending_auth import get_pending_user
    current_user = get_pending_user(request, db)
    
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado. Faça o cadastro novamente."
        )
    
    try:
        import mercadopago
        
        # Inicializar SDK
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        
        plan = PLANS.get(payment_data.plan, PLANS["pro"])
        
        # Preparar dados do pagamento
        payment_info = {
            "transaction_amount": float(plan["price"]),
            "description": f"RoboTrader - Plano {plan['name']}",
            "payment_method_id": "pix" if "pix" in payment_data.payment_method else "credit_card",
            "payer": {
                "email": current_user.email,
                "first_name": current_user.first_name,
                "last_name": current_user.last_name
            }
        }
        
        # Criar pagamento
        payment_response = sdk.payment().create(payment_info)
        payment_result = payment_response["response"]
        
        # Salvar no banco
        db_payment = Payment(
            user_id=current_user.id,
            amount=Decimal(str(plan["price"])),
            currency="BRL" if "pix" in payment_data.payment_method else "USD",
            status="pending",
            gateway="mercadopago",
            gateway_payment_id=str(payment_result.get("id")),
            pix_qr_code=payment_result.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code"),
            pix_copy_paste=payment_result.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64")
        )
        
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
        
        return {
            "payment_id": db_payment.id,
            "status": payment_result.get("status"),
            "amount": plan["price"],
            "currency": "BRL",
            "pix_qr_code": payment_result.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code"),
            "pix_copy_paste": payment_result.get("point_of_interaction", {}).get("transaction_data", {}).get("qr_code_base64"),
            "mercadopago_id": payment_result.get("id")
        }
        
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="MercadoPago SDK não instalado. Execute: pip install mercadopago"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar pagamento MercadoPago: {str(e)}"
        )

@router.post("/mercadopago/webhook")
async def mercadopago_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook do MercadoPago - PRODUÇÃO - Atualiza subscription AUTOMATICAMENTE"""
    
    try:
        body = await request.json()
        print(f"📨 Webhook MercadoPago recebido: {body.get('type')}")
        
        # Verificar tipo de notificação
        notification_type = body.get("type")
        
        if notification_type == "payment":
            payment_id = body.get("data", {}).get("id")
            
            if not payment_id:
                return {"status": "ok", "message": "No payment_id"}
            
            # Buscar informações do pagamento no MercadoPago
            import mercadopago
            sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
            payment_info = sdk.payment().get(int(payment_id))
            
            if payment_info["status"] == 200:
                payment_data = payment_info["response"]
                payment_status = payment_data.get("status")
                external_ref = payment_data.get("external_reference", "")
                payer_email = payment_data.get("payer", {}).get("email")
                
                print(f"💳 Pagamento {payment_id}: {payment_status}")
                print(f"📧 Email: {payer_email}")
                print(f"🔖 Ref: {external_ref}")
                
                # Extrair user_id e plan da external_reference
                # Formato: "user_123_plan_pro"
                if "user_" in external_ref and "_plan_" in external_ref:
                    parts = external_ref.split("_")
                    user_id = int(parts[1])
                    plan = parts[3]
                    
                    if payment_status == "approved":
                        # Buscar usuário
                        user = db.query(User).filter(User.id == user_id).first()
                        
                        if user:
                            # Criar/Atualizar subscription
                            existing_sub = db.query(Subscription).filter(
                                Subscription.user_id == user_id
                            ).first()
                            
                            if existing_sub:
                                existing_sub.plan = plan
                                existing_sub.status = "active"
                                existing_sub.payment_method = "mercadopago"
                                print(f"✅ Subscription atualizada: User {user_id} → {plan}")
                            else:
                                new_sub = Subscription(
                                    user_id=user_id,
                                    plan=plan,
                                    status="active",
                                    payment_method="mercadopago",
                                    amount=1.00 if plan == "pro" else 5.00,
                                    currency="BRL"
                                )
                                db.add(new_sub)
                                print(f"✅ Subscription criada: User {user_id} → {plan}")
                            
                            db.commit()
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Erro no webhook MercadoPago: {e}")
        return {"status": "error", "message": str(e)}

# ========================================
# STRIPE - CARTÃO INTERNACIONAL
# ========================================

@router.post("/stripe/create-checkout-session")
async def create_stripe_checkout(
    request: Request,
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    """Criar sessão de checkout do Stripe - ACEITA PENDING USER"""
    
    # Pegar usuário (pode ser pending ou logado)
    from ..utils.pending_auth import get_pending_user
    current_user = get_pending_user(request, db)
    
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado. Faça o cadastro novamente."
        )
    
    try:
        import stripe
        
        stripe.api_key = STRIPE_SECRET_KEY
        
        plan = PLANS.get(payment_data.plan, PLANS["pro"])
        
        # Criar sessão de checkout
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(plan["price"] * 100),  # Em centavos
                    'product_data': {
                        'name': f'RoboTrader - Plano {plan["name"]}',
                        'description': f'{plan["bots_limit"]} bots simultâneos',
                    },
                    'recurring': {
                        'interval': 'month'
                    }
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:8001/payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:8001/payment/cancelled',
            metadata={
                'user_id': current_user.id,
                'plan': payment_data.plan
            }
        )
        
        # Salvar pagamento pendente no banco
        db_payment = Payment(
            user_id=current_user.id,
            amount=Decimal(str(plan["price"])),
            currency="USD",
            status="pending",
            gateway="stripe",
            gateway_payment_id=checkout_session.id
        )
        
        db.add(db_payment)
        db.commit()
        
        return {
            "checkout_url": checkout_session.url,
            "session_id": checkout_session.id
        }
        
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="Stripe SDK não instalado. Execute: pip install stripe"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar checkout Stripe: {str(e)}"
        )

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Webhook do Stripe - PRODUÇÃO - Atualiza subscription AUTOMATICAMENTE"""
    
    try:
        import stripe
        import json
        
        stripe.api_key = STRIPE_SECRET_KEY
        
        payload = await request.body()
        event = json.loads(payload)
        
        print(f"📨 Webhook Stripe recebido: {event.get('type')}")
        
        # Processar checkout completado
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            metadata = session.get('metadata', {})
            
            user_id = int(metadata.get('user_id', 0))
            plan = metadata.get('plan', 'pro')
            
            print(f"💳 Checkout completado: User {user_id} → {plan}")
            
            if user_id:
                # Buscar usuário
                user = db.query(User).filter(User.id == user_id).first()
                
                if user:
                    # Criar/Atualizar subscription
                    existing_sub = db.query(Subscription).filter(
                        Subscription.user_id == user_id
                    ).first()
                    
                    if existing_sub:
                        existing_sub.plan = plan
                        existing_sub.status = "active"
                        existing_sub.payment_method = "stripe"
                        existing_sub.stripe_subscription_id = session.get('subscription')
                        print(f"✅ Subscription atualizada: User {user_id} → {plan}")
                    else:
                        new_sub = Subscription(
                            user_id=user_id,
                            plan=plan,
                            status="active",
                            payment_method="stripe",
                            amount=1.00 if plan == "pro" else 5.00,
                            currency="BRL",
                            stripe_subscription_id=session.get('subscription')
                        )
                        db.add(new_sub)
                        print(f"✅ Subscription criada: User {user_id} → {plan}")
                    
                    db.commit()
        
        # Assinatura cancelada
        elif event['type'] == 'customer.subscription.deleted':
            subscription_id = event['data']['object']['id']
            
            subscription = db.query(Subscription).filter(
                Subscription.stripe_subscription_id == subscription_id
            ).first()
            
            if subscription:
                subscription.status = "cancelled"
                print(f"❌ Subscription cancelada: {subscription_id}")
                db.commit()
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"❌ Erro no webhook Stripe: {e}")
        return {"status": "error", "message": str(e)}

# ========================================
# ENDPOINTS AUXILIARES
# ========================================

@router.get("/my-subscription", response_model=SubscriptionResponse)
async def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter assinatura atual do usuário"""
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma assinatura ativa encontrada"
        )
    
    return subscription

@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancelar assinatura do usuário"""
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == "active"
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma assinatura ativa para cancelar"
        )
    
    # Cancelar no gateway
    try:
        if subscription.stripe_subscription_id:
            import stripe
            stripe.api_key = STRIPE_SECRET_KEY
            stripe.Subscription.delete(subscription.stripe_subscription_id)
        
        # MercadoPago não precisa cancelar (pagamento único)
        
    except Exception as e:
        print(f"Erro ao cancelar no gateway: {e}")
    
    # Atualizar no banco
    subscription.status = "cancelled"
    subscription.cancelled_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Assinatura cancelada com sucesso"}

@router.get("/payment-history", response_model=list[PaymentResponse])
async def get_payment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Histórico de pagamentos do usuário"""
    
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).order_by(Payment.created_at.desc()).all()
    
    return payments




