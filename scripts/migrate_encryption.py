#!/usr/bin/env python3
"""
Script para re-criptografar API Keys com nova chave

⚠️  ATENÇÃO: Execute APENAS UMA VEZ após gerar nova ENCRYPTION_KEY
Execute: python scripts/migrate_encryption.py
"""

import sys
from pathlib import Path

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi_app.database import SessionLocal
from fastapi_app.models import ExchangeAPIKey
from cryptography.fernet import Fernet
import base64
import os

print("="*70)
print("  MIGRAÇÃO DE CRIPTOGRAFIA - RE-ENCRYPT API KEYS")
print("="*70)
print()

# Chave ANTIGA (hardcoded)
OLD_KEY = "dev-encryption-key-change-in-production"
old_fernet_key = base64.urlsafe_b64encode(OLD_KEY.encode().ljust(32)[:32])
old_fernet = Fernet(old_fernet_key)

# Chave NOVA (do .env)
NEW_KEY = os.getenv('ENCRYPTION_KEY')

if not NEW_KEY:
    print("❌ ERRO: ENCRYPTION_KEY não definida no .env!")
    print("Execute: python scripts/generate_encryption_key.py")
    sys.exit(1)

if NEW_KEY == OLD_KEY:
    print("⚠️  AVISO: Nova chave é igual à antiga!")
    print("Gere uma nova chave: python scripts/generate_encryption_key.py")
    sys.exit(1)

# Criar novo Fernet
if len(NEW_KEY) == 44 and NEW_KEY.endswith('='):
    new_fernet_key = NEW_KEY.encode()
else:
    new_fernet_key = base64.urlsafe_b64encode(NEW_KEY.encode().ljust(32)[:32])

new_fernet = Fernet(new_fernet_key)

print(f"✅ Nova chave configurada")
print()

# Conectar banco
db = SessionLocal()

try:
    # Buscar TODAS as API Keys
    api_keys = db.query(ExchangeAPIKey).all()
    
    if not api_keys:
        print("ℹ️  Nenhuma API Key encontrada no banco.")
        print("   Migração não necessária.")
        sys.exit(0)
    
    print(f"Encontradas {len(api_keys)} API Key(s) para re-criptografar")
    print()
    
    # Confirmar
    resposta = input("Deseja continuar? (sim/não): ").lower()
    
    if resposta not in ['sim', 's', 'yes', 'y']:
        print("Operação cancelada.")
        sys.exit(0)
    
    print()
    print("Re-criptografando...")
    print()
    
    success_count = 0
    error_count = 0
    
    for api_key in api_keys:
        try:
            # Descriptografar com chave ANTIGA
            api_key_plain = old_fernet.decrypt(api_key.api_key_encrypted.encode()).decode()
            secret_plain = old_fernet.decrypt(api_key.secret_key_encrypted.encode()).decode()
            
            # Re-criptografar com chave NOVA
            api_key.api_key_encrypted = new_fernet.encrypt(api_key_plain.encode()).decode()
            api_key.secret_key_encrypted = new_fernet.encrypt(secret_plain.encode()).decode()
            
            db.commit()
            
            print(f"✅ Re-criptografada: {api_key.user_id} - {api_key.exchange}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Erro ao re-criptografar {api_key.id}: {e}")
            error_count += 1
            db.rollback()
    
    print()
    print("="*70)
    print(f"✅ Sucesso: {success_count}")
    print(f"❌ Erros: {error_count}")
    print("="*70)
    print()
    
    if success_count > 0:
        print("🎉 Migração concluída com sucesso!")
        print()
        print("📝 Próximos passos:")
        print("1. Reinicie os serviços (pm2 restart all)")
        print("2. Teste login e acesso às API Keys")
        print("3. Verifique logs de erro")
    
finally:
    db.close()





