"""
Endpoint para verificar status de pagamento
Usado pelo polling automático
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from datetime import datetime

from ..database import get_db
from ..models_payment import Payment

router = APIRouter(prefix="/api/payments-public", tags=["verificacao-pagamento"])

# Chave MercadoPago
MERCADOPAGO_ACCESS_TOKEN = "APP_USR-7940373206085562-102818-e0b751adbf15c2d81e094a3dc01b0cef-2953317711"

@router.get("/check-payment/{payment_id}")
async def check_payment_status(payment_id: int, db: Session = Depends(get_db)):
    """Verificar status do pagamento no MercadoPago"""
    
    try:
        # Buscar pagamento no banco
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        
        if not payment:
            return {"status": "not_found"}
        
        # Se já foi aprovado, retornar
        if payment.status == "approved":
            return {"status": "approved", "payment_id": payment_id}
        
        # Verificar no MercadoPago
        import mercadopago
        sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)
        
        # Buscar pagamento no MercadoPago
        mp_payment = sdk.payment().get(int(payment.gateway_payment_id))
        
        if mp_payment["status"] == 200:
            mp_status = mp_payment["response"]["status"]
            
            # Se foi aprovado, atualizar banco
            if mp_status == "approved":
                payment.status = "approved"
                payment.paid_at = datetime.now()
                db.commit()
                
                return {"status": "approved", "payment_id": payment_id}
            else:
                return {"status": mp_status, "payment_id": payment_id}
        
        return {"status": payment.status, "payment_id": payment_id}
        
    except Exception as e:
        print(f"Erro ao verificar pagamento: {e}")
        return {"status": "error", "message": str(e)}

