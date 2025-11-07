"""
SQLAlchemy Models - Compatíveis com Django models existentes
"""

from sqlalchemy import Boolean, Column, Integer, String, Numeric, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """Usuário - Compatível com auth_user do Django"""
    __tablename__ = "auth_user"
    
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(128))  # Django usa senha hasheada
    last_login = Column(DateTime, nullable=True)
    is_superuser = Column(Boolean, default=False)
    username = Column(String(150), unique=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    email = Column(String(254), unique=True, index=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, server_default=func.now())
    
    # Campos adicionais (brasileiros)
    cpf = Column(String(14), unique=True, index=True, nullable=True)  # 000.000.000-00
    celular = Column(String(15), nullable=True)  # (00) 00000-0000
    
    # Relationships
    api_keys = relationship("ExchangeAPIKey", back_populates="user")
    bot_configs = relationship("BotConfiguration", back_populates="user")
    trades = relationship("Trade", back_populates="user")


class ExchangeAPIKey(Base):
    """API Keys das exchanges - Compatível com users_exchangeapikey"""
    __tablename__ = "users_exchangeapikey"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    exchange = Column(String(20))
    api_key_encrypted = Column(Text)
    secret_key_encrypted = Column(Text)
    is_testnet = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="api_keys")


class BotConfiguration(Base):
    """Configuração do bot - Compatível com bot_configurations"""
    __tablename__ = "bot_configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    name = Column(String(100))
    exchange = Column(String(20))
    symbols = Column(JSON)  # Lista de símbolos
    capital = Column(Numeric(12, 2))
    strategy = Column(String(20))
    timeframe = Column(String(5), default='15m')
    stop_loss_percent = Column(Numeric(5, 3), default=1.5)
    take_profit_percent = Column(Numeric(5, 3), default=3.0)
    is_active = Column(Boolean, default=False)
    is_testnet = Column(Boolean, default=True)
    # ✅ NOVO: Velocidade do bot
    analysis_interval = Column(Integer, default=5)  # segundos (1-60)
    hunter_mode = Column(Boolean, default=False)  # Modo caçador
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="bot_configs")
    trades = relationship("Trade", back_populates="bot_config")


class Trade(Base):
    """Histórico de trades - Compatível com trades"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    bot_config_id = Column(Integer, ForeignKey("bot_configurations.id"), nullable=True)
    exchange = Column(String(20))
    symbol = Column(String(20))
    side = Column(String(4))  # buy/sell
    entry_price = Column(Numeric(20, 8))
    exit_price = Column(Numeric(20, 8), nullable=True)
    quantity = Column(Numeric(20, 8))
    profit_loss = Column(Numeric(12, 2), nullable=True)
    profit_loss_percent = Column(Numeric(8, 2), nullable=True)
    entry_time = Column(DateTime)
    exit_time = Column(DateTime, nullable=True)
    status = Column(String(10), default='open')  # open/closed
    highest_price = Column(Numeric(20, 8), nullable=True)  # Trailing stop
    
    # Relationships
    user = relationship("User", back_populates="trades")
    bot_config = relationship("BotConfiguration", back_populates="trades")


