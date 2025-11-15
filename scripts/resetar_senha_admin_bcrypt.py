#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resetar Senha Admin com BCRYPT
Garante compatibilidade 100%
"""

import sys
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

print("="*70)
print("  RESETAR SENHA ADMIN - BCRYPT")
print("="*70)
print()

from fastapi_app.database import SessionLocal
from fastapi_app.models import User
from passlib.context import CryptContext

# Usar APENAS bcrypt (mais compatível)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

# Buscar admin
admin = db.query(User).filter(User.email == "admin@robotrader.com").first()

if not admin:
    print("[ERRO] Admin nao encontrado!")
    db.close()
    sys.exit(1)

print(f"[OK] Admin: {admin.email} (ID: {admin.id})")
print()

# Nova senha
nova_senha = "admin123"

print(f"Gerando hash BCRYPT para: {nova_senha}")
print()

# Gerar hash BCRYPT
novo_hash = pwd_context.hash(nova_senha)

print("Hash gerado:")
print(f"  {novo_hash[:50]}...")
print(f"  Tamanho: {len(novo_hash)}")
print(f"  Algoritmo: BCRYPT")
print()

# Testar hash
print("Testando hash...")
if pwd_context.verify(nova_senha, novo_hash):
    print("[OK] Hash funciona!")
    print()
else:
    print("[ERRO] Hash nao funciona!")
    sys.exit(1)

# Salvar no banco
print("Salvando no banco...")
admin.password = novo_hash
db.commit()

print("[OK] Senha resetada com sucesso!")
print()

print("="*70)
print("  CONCLUIDO!")
print("="*70)
print()
print("Credenciais:")
print("  Email: admin@robotrader.com")
print("  Senha: admin123")
print()
print("Algoritmo: BCRYPT (100% compativel)")
print()
print("Tente fazer login novamente!")
print()

db.close()



