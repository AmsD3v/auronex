from fastapi_app.database import get_db
from fastapi_app.models_payment import Subscription

db = next(get_db())

user_id = 61

sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()

if sub:
    print(f"Usuario {user_id}:")
    print(f"  Plano: {sub.plan}")
    print(f"  Status: {sub.status}")
    print(f"  Method: {sub.payment_method}")
else:
    print(f"Usuario {user_id}: SEM subscription")
    print("Criando subscription PRO...")
    
    new_sub = Subscription(
        user_id=user_id,
        plan="pro",
        status="active",
        payment_method="paid",
        amount=1.00,
        currency="BRL"
    )
    
    db.add(new_sub)
    db.commit()
    print("✅ Subscription PRO criada!")




