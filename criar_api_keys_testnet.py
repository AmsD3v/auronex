"""
Criar API Keys TESTNET para Paper Trading
"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import ExchangeAPIKey, User
from fastapi_app.utils.encryption import encrypt_data

db = SessionLocal()

# Buscar usuário (74 ou 1)
user = db.query(User).filter(User.id == 74).first()
if not user:
    user = db.query(User).filter(User.id == 1).first()

if not user:
    print("❌ Nenhum usuário encontrado!")
    db.close()
    exit(1)

print(f"Usuário: {user.email}")

# Deletar API Keys antigas (evitar duplicatas)
db.query(ExchangeAPIKey).filter(ExchangeAPIKey.user_id == user.id).delete()

# 1. BINANCE TESTNET
binance_key = ExchangeAPIKey(
    user_id=user.id,
    exchange='binance',
    api_key_encrypted=encrypt_data('testnet_api_key_fake'),
    secret_key_encrypted=encrypt_data('testnet_secret_fake'),
    is_active=True,
    is_testnet=True
)
db.add(binance_key)

# 2. MERCADO BITCOIN (não tem testnet, mas vamos marcar)
mb_key = ExchangeAPIKey(
    user_id=user.id,
    exchange='mercadobitcoin',
    api_key_encrypted=encrypt_data('mb_api_fake'),
    secret_key_encrypted=encrypt_data('mb_secret_fake'),
    is_active=True,
    is_testnet=True
)
db.add(mb_key)

db.commit()

print("\n✅ API Keys TESTNET criadas!")
print("  - Binance Testnet")
print("  - Mercado Bitcoin")
print("\nPaper Trading configurado!")

db.close()

