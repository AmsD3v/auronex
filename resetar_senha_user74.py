"""Resetar senha usuario 74 - SIMPLES"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import User

db = SessionLocal()

user = db.query(User).filter(User.id == 74).first()

if user:
    # Hash conhecido de "123456" 
    user.password_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eo7F3qBPcfCi"
    
    db.commit()
    
    print(f"Usuario: {user.email}")
    print(f"Nome: {user.first_name} {user.last_name}")
    print(f"\nSenha resetada para: 123456")
    print("\nFaca login agora!")
else:
    print("Usuario 74 nao encontrado")

db.close()

