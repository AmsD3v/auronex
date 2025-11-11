"""Criar usuario de teste com senha conhecida"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import User
from datetime import datetime

db = SessionLocal()

# Deletar usuario teste se existir
db.query(User).filter(User.email == "teste@auronex.com").delete()

# Criar novo
user = User(
    email="teste@auronex.com",
    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eo7F3qBPcfCi",  # senha: teste123
    first_name="Usuario",
    last_name="Teste",
    is_active=True,
    is_staff=False,
    is_superuser=False,
    created_at=datetime.now()
)

db.add(user)
db.commit()

print(f"Usuario criado:")
print(f"  Email: teste@auronex.com")
print(f"  Senha: teste123")
print(f"  Nome: Usuario Teste")
print("\nFaca login com este usuario!")

db.close()
