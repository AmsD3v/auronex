#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resetar Senha Admin - MÉTODO DJANGO
Usa o mesmo método que já funciona
"""

import sys
import io
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*70)
print("  RESETAR SENHA ADMIN - METODO DJANGO")
print("="*70)
print()

# Usar diretamente o Django hasher
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas.settings')

try:
    import django
    django.setup()
    from django.contrib.auth.models import User as DjangoUser
    
    print("[OK] Django carregado")
    print()
    
    # Buscar admin
    admin = DjangoUser.objects.filter(email="admin@robotrader.com").first()
    
    if not admin:
        print("[ERRO] Admin nao encontrado!")
        sys.exit(1)
    
    print(f"[OK] Admin: {admin.email} (ID: {admin.id})")
    print()
    
    # Resetar senha
    nova_senha = "admin123"
    admin.set_password(nova_senha)
    admin.save()
    
    print(f"[OK] Senha resetada para: {nova_senha}")
    print()
    print("Hash gerado:")
    print(f"  {admin.password[:50]}...")
    print()
    
    # Testar
    if admin.check_password(nova_senha):
        print("[OK] Senha funciona!")
    else:
        print("[ERRO] Senha nao funciona!")
    
    print()
    print("="*70)
    print("  SUCESSO!")
    print("="*70)
    print()
    print("Credenciais:")
    print("  Email: admin@robotrader.com")
    print("  Senha: admin123")
    print()
    
except Exception as e:
    print(f"[ERRO] Falha Django: {e}")
    print()
    print("Usando metodo direto no SQLite...")
    print()
    
    import sqlite3
    from passlib.hash import django_pbkdf2_sha256
    
    # Hash Django padrão
    novo_hash = django_pbkdf2_sha256.hash("admin123")
    
    # Conectar SQLite
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Atualizar senha
    cursor.execute("""
        UPDATE auth_user 
        SET password = ? 
        WHERE email = 'admin@robotrader.com'
    """, (novo_hash,))
    
    conn.commit()
    
    print("[OK] Senha atualizada diretamente no SQLite")
    print(f"Hash: {novo_hash[:50]}...")
    print()
    print("Credenciais:")
    print("  Email: admin@robotrader.com")
    print("  Senha: admin123")
    print()
    
    conn.close()



