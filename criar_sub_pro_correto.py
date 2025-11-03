import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

user_id = 61

# Criar com todos os campos
c.execute("""
    INSERT INTO subscriptions 
    (user_id, plan, status, stripe_subscription_id, mercadopago_subscription_id, payment_method, amount, currency)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (user_id, 'pro', 'active', '', '', 'mercadopago', 1.00, 'BRL'))

conn.commit()
print("[OK] Subscription PRO criada!")

# Verificar
c.execute("SELECT plan, status FROM subscriptions WHERE user_id = ?", (user_id,))
result = c.fetchone()
print(f"Plano: {result}")

conn.close()

print("\nFACA LOGOUT E LOGIN NOVAMENTE!")
print("Badge PRO deve aparecer agora!")





