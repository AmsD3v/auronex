"""
Pydantic Schemas - Validação de dados
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ========================================
# AUTH SCHEMAS
# ========================================

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    first_name: str
    last_name: str
    # Campos opcionais para compatibilidade
    cpf: Optional[str] = None
    celular: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    
    class Config:
        from_attributes = True

# ========================================
# API KEYS SCHEMAS
# ========================================

class APIKeyCreate(BaseModel):
    exchange: str = Field(pattern="^[a-z]+$")  # minúsculo apenas
    api_key: str
    secret_key: str
    is_testnet: bool = False
    is_active: bool = True

class APIKeyResponse(BaseModel):
    id: int
    exchange: str
    is_testnet: bool
    is_active: bool
    created_at: datetime
    
    # NÃO retorna keys por segurança!
    
    class Config:
        from_attributes = True

# ========================================
# BOT CONFIGURATION SCHEMAS
# ========================================

class BotConfigCreate(BaseModel):
    name: str
    exchange: str
    symbols: List[str]
    capital: Optional[Decimal] = Decimal("0")  # Opcional - usa saldo real
    strategy: str = "mean_reversion"
    timeframe: str = "15m"
    stop_loss_percent: Decimal = Decimal("1.5")
    take_profit_percent: Decimal = Decimal("3.0")
    is_active: bool = False

class BotConfigUpdate(BaseModel):
    name: Optional[str] = None
    symbols: Optional[List[str]] = None
    capital: Optional[Decimal] = None
    is_active: Optional[bool] = None

class BotConfigResponse(BaseModel):
    id: int
    name: str
    exchange: str
    symbols: List[str]
    capital: Decimal
    strategy: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========================================
# TRADE SCHEMAS
# ========================================

class TradeResponse(BaseModel):
    id: int
    symbol: str
    side: str
    entry_price: Decimal
    exit_price: Optional[Decimal]
    quantity: Decimal
    profit_loss: Optional[Decimal]
    status: str
    entry_time: datetime
    exit_time: Optional[datetime]
    
    class Config:
        from_attributes = True


