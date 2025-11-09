"""Tornar usuario admin"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import User

db = SessionLocal()

# User 74
user = db.query(User).filter(User.id == 74).first()

if user:
    print(f"Usuario: {user.email}")
    print(f"  Antes: is_superuser={user.is_superuser}, is_staff={user.is_staff}")
    
    user.is_superuser = True
    user.is_staff = True
    
    db.commit()
    
    print(f"  Depois: is_superuser={user.is_superuser}, is_staff={user.is_staff}")
    print("\n[OK] Usuario agora e ADMIN!")
else:
    print("Usuario nao encontrado")

db.close()

