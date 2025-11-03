"""
Models de Pagamento - Assinaturas e Transações
"""

from sqlalchemy import Boolean, Column, Integer, String, Numeric, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Subscription(Base):
    """Assinaturas de usuários - TABELA FASTAPI PRÓPRIA"""
    __tablename__ = "subscriptions_fastapi"  # Nova tabela (sem conflito com Django)
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    
    # Plano
    plan = Column(String(20), nullable=False, default="free")  # free, pro, premium
    status = Column(String(20), nullable=False, default="active")  # active, cancelled, expired, pending
    
    # Pagamento
    payment_method = Column(String(20), nullable=True, default="none")  # stripe, mercadopago, none
    amount = Column(Numeric(10, 2), nullable=True, default=0)  # Valor mensal
    currency = Column(String(3), nullable=True, default="BRL")  # BRL, USD
    
    # Controle
    started_at = Column(DateTime, nullable=False, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    
    # IDs externos (NULLABLE para evitar erros!)
    stripe_subscription_id = Column(String(100), nullable=True, default=None)
    mercadopago_subscription_id = Column(String(100), nullable=True, default=None)
    
    # Não usar relationship (causa erro de import circular)


class Payment(Base):
    """Histórico de pagamentos"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    
    # Detalhes
    amount = Column(Numeric(10, 2))
    currency = Column(String(3), default="USD")
    status = Column(String(20))  # pending, approved, rejected, refunded
    
    # Gateway
    gateway = Column(String(20))  # stripe, mercadopago
    gateway_payment_id = Column(String(100))  # ID na gateway
    
    # PIX (se aplicável)
    pix_qr_code = Column(Text, nullable=True)
    pix_qr_code_base64 = Column(Text, nullable=True)
    pix_copy_paste = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    paid_at = Column(DateTime, nullable=True)
    
    # Não usar relationship (causa erro de import circular)










