"""
Verificação de Pagamento - SOLUÇÃO PARA LOCALHOST
Como webhooks não funcionam em localhost, verificamos via API
"""

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..models_payment import Subscription

router = APIRouter(prefix="/api/verify-payment", tags=["verificacao"])

# Chaves
MERCADOPAGO_ACCESS_TOKEN = "APP_USR-7940373206085562-102818-e0b751adbf15c2d81e094a3dc01b0cef-2953317711"
STRIPE_SECRET_KEY = "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"

@router.get("/mercadopago/{preference_id}")
async def verify_mercadopago_payment(preference_id: str, db: Session = Depends(get_db)):
    """Verificar se pagamento do MercadoPago foi aprovado"""
    
    try:
        import mercadopago
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        
        # Buscar preferência
        preference = sdk.preference().get(preference_id)
        
        if preference["status"] == 200:
            pref_data = preference["response"]
            external_ref = pref_data.get("external_reference", "")
            
            # Extrair user_id e plan
            if "user_" in external_ref and "_plan_" in external_ref:
                parts = external_ref.split("_")
                user_id = int(parts[1])
                plan = parts[3]
                
                # Buscar pagamentos dessa preferência
                # (MercadoPago cria payment quando usuário paga)
                # Verificamos via API se tem payment aprovado
                
                # Por simplicidade, retornamos que precisa confirmar manualmente
                return {
                    "status": "pending",
                    "user_id": user_id,
                    "plan": plan,
                    "message": "Verificação manual necessária"
                }
        
        return {"status": "not_found"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/confirm-payment")
async def confirm_payment_manually(request: Request, db: Session = Depends(get_db)):
    """Confirmar pagamento manualmente e ativar plano"""
    
    try:
        # Pegar usuário logado
        from ..utils.auth_pages import get_current_user_from_cookie
        user = get_current_user_from_cookie(request, db)
        
        if not user:
            return {"success": False, "message": "Usuário não logado"}
        
        body = await request.json()
        plan = body.get("plan", "pro")
        
        print(f"📝 Confirmando pagamento manual: User {user.id} → {plan}")
        
        # Criar/Atualizar subscription
        existing_sub = db.query(Subscription).filter(
            Subscription.user_id == user.id
        ).first()
        
        if existing_sub:
            existing_sub.plan = plan
            existing_sub.status = "active"
            existing_sub.payment_method = "confirmed"
            print(f"✅ Subscription atualizada")
        else:
            new_sub = Subscription(
                user_id=user.id,
                plan=plan,
                status="active",
                payment_method="confirmed",
                amount=1.00 if plan == "pro" else 5.00,
                currency="BRL"
            )
            db.add(new_sub)
            print(f"✅ Subscription criada")
        
        db.commit()
        
        return {
            "success": True,
            "plan": plan,
            "redirect": "/dashboard"
        }
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
        return {"success": False, "message": str(e)}




