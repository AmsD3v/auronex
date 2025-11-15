#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug Login - Verificar usuário e senha
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
from fastapi_app.auth import verify_password, get_password_hash

print("="*70)
print("  DEBUG LOGIN - VERIFICACAO COMPLETA")
print("="*70)
print()

db = SessionLocal()

# Buscar usuário admin
email = "admin@robotrader.com"
print(f"Buscando usuario: {email}")
print()

user = db.query(User).filter(User.email == email).first()

if not user:
    print("[ERRO] Usuario NAO encontrado no banco!")
    print()
    print("Usuarios disponiveis:")
    all_users = db.query(User).all()
    for u in all_users:
        print(f"  - {u.email} (ID: {u.id})")
    print()
    db.close()
    sys.exit(1)

print("[OK] Usuario encontrado!")
print(f"  ID: {user.id}")
print(f"  Email: {user.email}")
print(f"  Nome: {user.first_name} {user.last_name}")
print(f"  Ativo: {user.is_active}")
print(f"  Staff: {user.is_staff}")
print(f"  Superuser: {user.is_superuser}")
print()

# Verificar hash
print("Hash da senha no banco:")
print(f"  Comeca com: {user.password[:30]}...")
print(f"  Tamanho: {len(user.password)} caracteres")
print()

# Identificar algoritmo
if user.password.startswith('$2b$') or user.password.startswith('$2a$'):
    print("  Algoritmo: BCRYPT")
elif user.password.startswith('$argon2'):
    print("  Algoritmo: ARGON2")
else:
    print("  Algoritmo: DESCONHECIDO")
print()

# Testar senha
senha_teste = "admin123"
print(f"Testando senha: '{senha_teste}'")
print()

try:
    resultado = verify_password(senha_teste, user.password)
    
    if resultado:
        print("[OK] SENHA CORRETA! Login deve funcionar.")
    else:
        print("[ERRO] SENHA INCORRETA!")
        print()
        print("Opcoes:")
        print("1. Senha no banco esta errada")
        print("2. Algoritmo de hash incompativel")
        print()
        print("Solucao: Resetar senha do admin")
        print("  python scripts/resetar_senha_admin.py")
    
except Exception as e:
    print(f"[ERRO] Falha ao verificar senha: {e}")
    print()
    print("Algoritmo de hash pode estar incompativel.")

print()
print("="*70)
print("  FIM DO DEBUG")
print("="*70)
print()

db.close()



