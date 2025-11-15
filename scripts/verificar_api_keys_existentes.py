#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar API Keys Existentes no Banco
"""

import sys
import io
from pathlib import Path

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*70)
print("  VERIFICANDO API KEYS EXISTENTES")
print("="*70)
print()

try:
    from fastapi_app.database import SessionLocal
    from fastapi_app.models import User, ExchangeAPIKey
    
    db = SessionLocal()
    
    # Buscar todos usuários
    users = db.query(User).all()
    
    print(f"Total de usuarios: {len(users)}")
    print()
    
    # Para cada usuário
    for user in users:
        api_keys = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == user.id
        ).all()
        
        if api_keys:
            print(f"Usuario: {user.email} (ID: {user.id})")
            print(f"API Keys: {len(api_keys)}")
            print()
            
            for key in api_keys:
                status = "Ativa" if key.is_active else "Inativa"
                testnet = "Testnet" if key.is_testnet else "Producao"
                
                print(f"  - {key.exchange.upper()}")
                print(f"    ID: {key.id}")
                print(f"    Tipo: {testnet}")
                print(f"    Status: {status}")
                print(f"    Criada: {key.created_at}")
                print()
    
    # Verificar total
    total_keys = db.query(ExchangeAPIKey).count()
    
    print("="*70)
    print(f"TOTAL DE API KEYS NO SISTEMA: {total_keys}")
    print("="*70)
    print()
    
    if total_keys == 0:
        print("[INFO] Nenhuma API Key configurada ainda.")
        print()
        print("Para adicionar:")
        print("  python scripts/configurar_api_keys.py")
        print()
    else:
        print("[OK] Sistema ja tem API Keys configuradas!")
        print()
        print("Opcoes:")
        print("1. Adicionar mais: python scripts/configurar_api_keys.py")
        print("2. Ativar bot com keys existentes")
        print()
    
    db.close()
    
except Exception as e:
    print(f"[ERRO] {e}")
    import traceback
    traceback.print_exc()






