"""Resetar senha de usuario"""
import sqlite3
import bcrypt

# Pedir email
email = input("Email do usuario: ")
nova_senha = input("Nova senha: ")

# Hash da senha (mesmo algoritmo do FastAPI)
senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()

# Atualizar no banco
db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()

cursor.execute("UPDATE auth_user SET password = ? WHERE email = ?", (senha_hash, email))
db.commit()

if cursor.rowcount > 0:
    print(f"\n[OK] Senha atualizada para: {email}")
    print(f"\nCredenciais:")
    print(f"  Email: {email}")
    print(f"  Senha: {nova_senha}")
    print(f"\nUse para fazer login!")
else:
    print(f"\n[ERRO] Usuario {email} nao encontrado!")

db.close()

