#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resetar Senha do Admin
"""

import sys
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from fastapi_app.database import SessionLocal
from fastapi_app.models import User
from fastapi_app.auth import get_password_hash

print("="*70)
print("  RESETAR SENHA DO ADMIN")
print("="*70)
print()

db = SessionLocal()

# Buscar admin
user = db.query(User).filter(User.email == "admin@robotrader.com").first()

if not user:
    print("[ERRO] Usuario admin@robotrader.com nao encontrado!")
    db.close()
    sys.exit(1)

print(f"[OK] Usuario encontrado: {user.email} (ID: {user.id})")
print()

# Nova senha
nova_senha = "admin123"
print(f"Resetando senha para: {nova_senha}")
print()

# Gerar hash (bcrypt)
novo_hash = get_password_hash(nova_senha)

print(f"Novo hash gerado:")
print(f"  Comeca com: {novo_hash[:30]}...")
print(f"  Tamanho: {len(novo_hash)} caracteres")
print()

# Atualizar no banco
user.password = novo_hash
db.commit()

print("[OK] Senha resetada com sucesso!")
print()
print("Credenciais:")
print(f"  Email: admin@robotrader.com")
print(f"  Senha: {nova_senha}")
print()
print("Tente fazer login novamente!")
print()

db.close()



