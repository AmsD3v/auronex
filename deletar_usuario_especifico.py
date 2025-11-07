"""Deletar usuario especifico"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import User, BotConfiguration, ExchangeAPIKey, Trade
from fastapi_app.models_payment import Subscription, Payment

db = SessionLocal()

email = "angelosilvaguitarrista@gmail.com"

user = db.query(User).filter(User.email == email).first()

if not user:
    print(f"Usuario {email} nao encontrado")
    db.close()
    exit()

user_id = user.id

print(f"Deletando usuario: {email} (ID: {user_id})")

# Deletar bots
bots = db.query(BotConfiguration).filter(BotConfiguration.user_id == user_id).all()
for bot in bots:
    db.delete(bot)
print(f"  - {len(bots)} bots deletados")

# Deletar API keys
keys = db.query(ExchangeAPIKey).filter(ExchangeAPIKey.user_id == user_id).all()
for key in keys:
    db.delete(key)
print(f"  - {len(keys)} API keys deletadas")

# Deletar trades
trades = db.query(Trade).filter(Trade.user_id == user_id).all()
for trade in trades:
    db.delete(trade)
print(f"  - {len(trades)} trades deletados")

# Deletar subscriptions
try:
    subs = db.query(Subscription).filter(Subscription.user_id == user_id).all()
    for sub in subs:
        db.delete(sub)
    print(f"  - {len(subs)} subscriptions deletadas")
except:
    pass

# Deletar payments
try:
    pays = db.query(Payment).filter(Payment.user_id == user_id).all()
    for pay in pays:
        db.delete(pay)
    print(f"  - {len(pays)} payments deletados")
except:
    pass

# Deletar usuario
db.delete(user)

db.commit()
db.close()

print(f"\n[OK] Usuario {email} DELETADO COMPLETAMENTE!")

