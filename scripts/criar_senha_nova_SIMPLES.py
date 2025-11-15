#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criar Senha Nova - SIMPLES com bcrypt
SEM Django, SEM complicação!
"""

import sys
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*70)
print("  CRIAR SENHA NOVA - BCRYPT SIMPLES")
print("="*70)
print()

# Bcrypt puro
import bcrypt

email = "admin@robotrader.com"
senha = "admin123"

print(f"Email: {email}")
print(f"Senha: {senha}")
print()

# Gerar hash bcrypt SIMPLES
print("Gerando hash bcrypt...")
senha_bytes = senha.encode('utf-8')
salt = bcrypt.gensalt()
hash_bcrypt = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

print(f"Hash gerado: {hash_bcrypt[:50]}...")
print(f"Algoritmo: BCRYPT puro")
print()

# Testar hash
print("Testando hash...")
if bcrypt.checkpw(senha_bytes, hash_bcrypt.encode('utf-8')):
    print("[OK] Hash funciona!")
else:
    print("[ERRO] Hash nao funciona!")
    sys.exit(1)

print()

# Atualizar no banco DIRETAMENTE
import sqlite3

print("Atualizando no banco SQLite...")

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Atualizar senha
cursor.execute("""
    UPDATE auth_user 
    SET password = ? 
    WHERE email = ?
""", (hash_bcrypt, email))

linhas_afetadas = cursor.rowcount
conn.commit()

print(f"[OK] {linhas_afetadas} linha(s) atualizada(s)")
print()

# Verificar
cursor.execute("SELECT id, email, password FROM auth_user WHERE email = ?", (email,))
row = cursor.fetchone()

if row:
    print("Verificacao no banco:")
    print(f"  ID: {row[0]}")
    print(f"  Email: {row[1]}")
    print(f"  Hash: {row[2][:50]}...")
    print()

conn.close()

print("="*70)
print("  SUCESSO!")
print("="*70)
print()
print("CREDENCIAIS:")
print(f"  Email: {email}")
print(f"  Senha: {senha}")
print()
print("Algoritmo: BCRYPT (simples e confiavel)")
print()
print("PROXIMOS PASSOS:")
print("1. Reinicie FastAPI (MATAR_TUDO.bat + TESTAR_SERVER_LOCAL...)")
print("2. Limpe cache do navegador (Ctrl+Shift+Delete)")
print("3. Faca login")
print()
print("DEVE FUNCIONAR!")
print()



