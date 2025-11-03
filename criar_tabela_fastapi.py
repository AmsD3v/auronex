from fastapi_app.database import engine, Base
from fastapi_app.models_payment import Subscription, Payment
import sqlite3

print("Criando tabela subscriptions_fastapi...")
Base.metadata.create_all(bind=engine)
print("[OK] Tabela criada!")

# Verificar tabelas
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%subscription%'")
tables = c.fetchall()
print("Tabelas de subscription:", tables)

# Criar subscription PRO para usuário 61
print("\nCriando subscription PRO para usuario 61...")
c.execute("""
    INSERT INTO subscriptions_fastapi (user_id, plan, status, payment_method, amount, currency)
    VALUES (61, 'pro', 'active', 'mercadopago', 1.00, 'BRL')
""")
conn.commit()
print("[OK] Subscription PRO criada!")

# Verificar
c.execute("SELECT plan, status FROM subscriptions_fastapi WHERE user_id = 61")
result = c.fetchone()
print(f"Plano do usuario 61: {result}")

conn.close()

print("\n========================================")
print("  TABELA FASTAPI CRIADA!")
print("========================================")
print("\nAGORA:")
print("1. Reinicie o FastAPI")
print("2. Faca logout e login")
print("3. Badge PRO deve aparecer!")





