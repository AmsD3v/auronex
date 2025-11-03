import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Criar subscription PRO
c.execute("""
    INSERT INTO subscriptions (user_id, plan, status)
    VALUES (61, 'pro', 'active')
""")

conn.commit()
print("[OK] Subscription PRO criada para usuario 61!")

# Verificar
c.execute("SELECT plan, status FROM subscriptions WHERE user_id = 61")
result = c.fetchone()
print(f"Plano: {result}")

conn.close()





