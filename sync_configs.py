"""
Sync configurações entre servidores
NÃO sincroniza senhas (segurança)
"""
import json
from fastapi_app.database import SessionLocal
from fastapi_app.models import User

db = SessionLocal()

# Exportar estrutura dos usuários (SEM senhas)
users = db.query(User).all()

export = []
for u in users:
    export.append({
        "email": u.email,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "is_active": u.is_active,
        "is_staff": u.is_staff,
        "is_superuser": u.is_superuser,
        # SENHA NÃO VAI!
    })

with open('users_export.json', 'w') as f:
    json.dump(export, f, indent=2)

print(f"Exportado {len(export)} usuarios")
print("Arquivo: users_export.json")
print("\nNOTA: Senhas NAO exportadas (segurança)")
print("Cada servidor deve ter senhas próprias!")

db.close()

