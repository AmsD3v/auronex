"""Verificar usuários no banco"""
import sqlite3

db = sqlite3.connect('db.sqlite3')
cursor = db.cursor()

print("Usuarios cadastrados:")
print("="*60)

cursor.execute("SELECT id, email, first_name, is_active FROM auth_user")
users = cursor.fetchall()

for user in users:
    print(f"ID: {user[0]}")
    print(f"Email: {user[1]}")
    print(f"Nome: {user[2]}")
    print(f"Ativo: {user[3]}")
    print("-"*60)

print(f"\nTotal: {len(users)} usuarios")
db.close()

