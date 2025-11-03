"""
Modelo para tokens de recuperação de senha
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime, timedelta
from .database import Base

class PasswordResetToken(Base):
    """Tokens para recuperação de senha"""
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String(100), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        """Verificar se token ainda é válido"""
        return not self.used and datetime.utcnow() < self.expires_at



