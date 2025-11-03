"""
Database configuration - SQLAlchemy
Compatível com os dados do Django existente
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Usar o MESMO banco SQLite do Django!
DATABASE_URL = f"sqlite:///{Path(__file__).parent.parent / 'db.sqlite3'}"

# Criar engine com configurações otimizadas
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,  # SQLite com múltiplas threads
        "timeout": 30,  # Timeout de 30s
    },
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_recycle=3600,  # Recicla conexões a cada hora
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency para rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


