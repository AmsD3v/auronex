from fastapi_app.database import get_db
from fastapi_app.models_payment import Subscription

db = next(get_db())

print("Testando acesso a subscriptions_fastapi...")

try:
    subs = db.query(Subscription).all()
    print(f"[OK] Total subscriptions: {len(subs)}")
    
    for s in subs:
        print(f"  User {s.user_id}: Plano {s.plan}, Status {s.status}")
        
except Exception as e:
    print(f"[ERRO] {e}")

print("\nTestando usuario 61...")
try:
    sub = db.query(Subscription).filter(Subscription.user_id == 61).first()
    if sub:
        print(f"[OK] Usuario 61: Plano {sub.plan}")
    else:
        print("[ERRO] Usuario 61 sem subscription")
except Exception as e:
    print(f"[ERRO] {e}")





