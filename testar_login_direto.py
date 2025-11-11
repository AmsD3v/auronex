"""Testar login diretamente no codigo"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

# Usuario 74
user = db.query(User).filter(User.email == "catheriine.fake@gmail.com").first()

if user:
    print(f"Usuario: {user.email}")
    print(f"Nome: {user.first_name} {user.last_name}")
    print(f"Hash armazenado: {user.password_hash[:50]}...")
    
    # Testar senhas comuns
    senhas = ["senha123", "123456", "password", "admin123", ""]
    
    for senha in senhas:
        try:
            if pwd_context.verify(senha, user.password_hash):
                print(f"\n[OK] SENHA CORRETA: '{senha}'")
                break
        except:
            pass
    else:
        print("\nNenhuma senha comum funcionou!")
        print("\nResetar senha manualmente no FastAPI:")
        print("  http://localhost:8001/admin/")
        print("  Editar usuario")
else:
    print("Usuario nao encontrado")

db.close()

