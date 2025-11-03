"""Execute este script para atualizar o usuário para plano PRO"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

# Atualizar
c.execute("""
    UPDATE subscriptions 
    SET plan='pro', status='active'
    WHERE user_id=61
""")

conn.commit()
print("[OK] Usuario 61 (aisha.rafa137@gmail.com) atualizado para PRO!")
print("Faca logout e login novamente para ver o badge PRO!")

conn.close()

