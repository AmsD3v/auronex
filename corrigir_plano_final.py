import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Buscar usuário
c.execute("SELECT id, email FROM auth_user WHERE email LIKE '%aisha%'")
users = c.fetchall()

print("Usuarios encontrados:", users)

if users:
    user_id = users[0][0]
    print(f"User ID: {user_id}")
    
    # Ver subscriptions atuais
    c.execute("SELECT id, plan, status FROM subscriptions WHERE user_id = ?", (user_id,))
    subs = c.fetchall()
    print(f"Subscriptions: {subs}")
    
    # Atualizar TODAS para PRO
    c.execute("UPDATE subscriptions SET plan='pro', status='active' WHERE user_id = ?", (user_id,))
    conn.commit()
    print("Atualizado!")
    
    # Verificar
    c.execute("SELECT plan, status FROM subscriptions WHERE user_id = ?", (user_id,))
    result = c.fetchall()
    print("Subscriptions atualizadas:", result)

conn.close()
print("\nFaca logout e login novamente!")





