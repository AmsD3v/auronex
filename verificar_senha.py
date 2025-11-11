"""Verificar e resetar senha do usuario"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

user = db.query(User).filter(User.email == "catheriine.fake@gmail.com").first()

if user:
    print(f"Usuario: {user.email}")
    print(f"Nome: {user.first_name} {user.last_name}")
    
    # Resetar senha para "senha123"
    nova_senha = "senha123"
    user.hashed_password = pwd_context.hash(nova_senha)
    
    db.commit()
    
    print(f"\nSenha resetada para: {nova_senha}")
    print("\nAgora teste login!")
else:
    print("Usuario nao encontrado")

db.close()

