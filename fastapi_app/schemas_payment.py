"""
Schemas de Pagamento - Validação de dados
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal

# ========================================
# SUBSCRIPTION SCHEMAS
# ========================================

class SubscriptionCreate(BaseModel):
    plan: str  # free, pro, premium
    payment_method: str  # stripe, mercadopago, pix
    
class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan: str
    status: str
    amount: Decimal
    currency: str
    started_at: datetime
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# ========================================
# PAYMENT SCHEMAS
# ========================================

class PaymentCreate(BaseModel):
    plan: str
    payment_method: str  # stripe, mercadopago_pix, mercadopago_card
    
class PaymentResponse(BaseModel):
    id: int
    amount: Decimal
    currency: str
    status: str
    gateway: str
    gateway_payment_id: str
    created_at: datetime
    paid_at: Optional[datetime]
    
    # PIX (se aplicável)
    pix_qr_code: Optional[str]
    pix_copy_paste: Optional[str]
    
    class Config:
        from_attributes = True

# ========================================
# WEBHOOK SCHEMAS
# ========================================

class StripeWebhook(BaseModel):
    """Webhook do Stripe"""
    type: str
    data: dict

class MercadoPagoWebhook(BaseModel):
    """Webhook do MercadoPago"""
    action: str
    data: dict
    type: str














