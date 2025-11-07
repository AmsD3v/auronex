"""Criar usuario de teste"""
import sys
sys.path.append('.')

from fastapi_app.database import SessionLocal
from fastapi_app.models import User
from fastapi_app.auth import get_password_hash

db = SessionLocal()

# Verificar se ja existe
existing = db.query(User).filter(User.email == "teste@auronex.com").first()

if existing:
    print(f"Usuario ja existe: {existing.email}")
    print(f"Resetando senha para: teste123")
    existing.password = get_password_hash("teste123")
    db.commit()
    print("Senha resetada!")
else:
    # Criar novo
    user = User(
        email="teste@auronex.com",
        password=get_password_hash("teste123"),
        first_name="Teste",
        last_name="Auronex",
        is_active=True,
        is_superuser=False
    )
    
    db.add(user)
    db.commit()
    print("Usuario criado!")

print("\nCredenciais:")
print("Email: teste@auronex.com")
print("Senha: teste123")
print("\nUse estas para fazer login!")

db.close()


