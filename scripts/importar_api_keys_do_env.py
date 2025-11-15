#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Importar API Keys do .env para o Banco de Dados
Criptografa e salva automaticamente
"""

import sys
import io
from pathlib import Path

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*70)
print("  IMPORTAR API KEYS DO .ENV PARA O BANCO")
print("="*70)
print()

# Carregar .env
import os
from dotenv import load_dotenv

load_dotenv()

print("[1/6] Carregando .env...")

# Verificar chaves de segurança
encryption_key = os.getenv('ENCRYPTION_KEY')
secret_key = os.getenv('SECRET_KEY')

if not encryption_key or not secret_key:
    print("[ERRO] ENCRYPTION_KEY ou SECRET_KEY não configuradas!")
    print("Configure o .env primeiro.")
    sys.exit(1)

print("[OK] Chaves de segurança encontradas")
print()

# Importar módulos
try:
    from fastapi_app.database import SessionLocal
    from fastapi_app.models import User, ExchangeAPIKey
    from fastapi_app.utils.encryption import encrypt_data
    print("[2/6] Módulos importados")
    print()
except Exception as e:
    print(f"[ERRO] Falha ao importar: {e}")
    sys.exit(1)

# Conectar banco
db = SessionLocal()

# Buscar usuário
print("[3/6] Buscando usuário admin...")
user = db.query(User).filter(User.email == "admin@robotrader.com").first()

if not user:
    print("[ERRO] Usuário admin@robotrader.com não encontrado!")
    print("Crie o usuário primeiro.")
    db.close()
    sys.exit(1)

print(f"[OK] Usuário: {user.email} (ID: {user.id})")
print()

# Exchanges configuradas no .env
exchanges_config = [
    ("binance", "BINANCE_TESTNET_API_KEY", "BINANCE_TESTNET_SECRET_KEY", True),
    ("binance", "BINANCE_API_KEY", "BINANCE_SECRET_KEY", False),
    ("bybit", "BYBIT_TESTNET_API_KEY", "BYBIT_TESTNET_SECRET_KEY", True),
    ("bybit", "BYBIT_API_KEY", "BYBIT_SECRET_KEY", False),
    ("mercadobitcoin", "MERCADOBITCOIN_API_KEY", "MERCADOBITCOIN_SECRET_KEY", False),
    ("okx", "OKX_API_KEY", "OKX_SECRET_KEY", False),
    ("kraken", "KRAKEN_API_KEY", "KRAKEN_SECRET_KEY", False),
    ("kucoin", "KUCOIN_API_KEY", "KUCOIN_SECRET_KEY", False),
    ("foxbit", "FOXBIT_API_KEY", "FOXBIT_SECRET_KEY", False),
]

print("[4/6] Importando API Keys do .env...")
print()

imported_count = 0
skipped_count = 0

for exchange_name, api_env, secret_env, is_testnet in exchanges_config:
    api_key_value = os.getenv(api_env)
    secret_key_value = os.getenv(secret_env)
    
    # Pular se vazio
    if not api_key_value or not secret_key_value:
        print(f"   [SKIP] {exchange_name.upper()} {'(Testnet)' if is_testnet else ''} - Vazio no .env")
        skipped_count += 1
        continue
    
    # Verificar se já existe
    existing = db.query(ExchangeAPIKey).filter(
        ExchangeAPIKey.user_id == user.id,
        ExchangeAPIKey.exchange == exchange_name,
        ExchangeAPIKey.is_testnet == is_testnet
    ).first()
    
    if existing:
        # Atualizar existente
        print(f"   [UPDATE] {exchange_name.upper()} {'(Testnet)' if is_testnet else ''} - Atualizando...")
        
        existing.api_key_encrypted = encrypt_data(api_key_value)
        existing.secret_key_encrypted = encrypt_data(secret_key_value)
        existing.is_active = True
        
        db.commit()
        imported_count += 1
        
    else:
        # Criar nova
        print(f"   [NEW] {exchange_name.upper()} {'(Testnet)' if is_testnet else ''} - Criando...")
        
        new_key = ExchangeAPIKey(
            user_id=user.id,
            exchange=exchange_name,
            api_key_encrypted=encrypt_data(api_key_value),
            secret_key_encrypted=encrypt_data(secret_key_value),
            is_testnet=is_testnet,
            is_active=True
        )
        
        db.add(new_key)
        db.commit()
        imported_count += 1

print()
print("[5/6] Testando conexões...")
print()

# Testar cada API Key
import ccxt

for exchange_name, api_env, secret_env, is_testnet in exchanges_config:
    api_key_value = os.getenv(api_env)
    secret_key_value = os.getenv(secret_env)
    
    if not api_key_value or not secret_key_value:
        continue
    
    try:
        # Mapa ccxt
        ccxt_map = {
            'mercadobitcoin': 'mercado',
            'gateio': 'gate',
        }
        ccxt_name = ccxt_map.get(exchange_name, exchange_name)
        
        # Criar exchange
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_key_value,
            'secret': secret_key_value,
            'enableRateLimit': True,
            'options': {
                'adjustForTimeDifference': True,  # ✅ Corrige diferença de horário
                'recvWindow': 60000,  # 60 segundos de tolerância
            }
        })
        
        if is_testnet:
            exchange.set_sandbox_mode(True)
        
        # Testar saldo
        balance = exchange.fetch_balance()
        usdt = balance.get('free', {}).get('USDT', 0) or balance.get('USDT', {}).get('free', 0) or 0
        brl = balance.get('free', {}).get('BRL', 0) or balance.get('BRL', {}).get('free', 0) or 0
        
        if usdt > 0:
            print(f"   [OK] {exchange_name.upper()} {'(Testnet)' if is_testnet else ''} - Saldo: ${usdt:.2f} USDT")
        elif brl > 0:
            print(f"   [OK] {exchange_name.upper()} - Saldo: R$ {brl:.2f} BRL")
        else:
            print(f"   [OK] {exchange_name.upper()} {'(Testnet)' if is_testnet else ''} - Conectado (saldo zero)")
        
    except Exception as e:
        error_msg = str(e)[:80]
        print(f"   [ERRO] {exchange_name.upper()} {'(Testnet)' if is_testnet else ''} - {error_msg}")

print()
print("[6/6] Finalizando...")
db.close()

print()
print("="*70)
print("  IMPORTACAO CONCLUIDA!")
print("="*70)
print()
print(f"API Keys importadas: {imported_count}")
print(f"Vazias (ignoradas): {skipped_count}")
print()
print("="*70)
print("  PROXIMOS PASSOS:")
print("="*70)
print()
print("1. Reinicie os servicos:")
print("   MATAR_TUDO.bat")
print("   TESTAR_SERVER_LOCAL_09_11_25.bat")
print()
print("2. Abra o dashboard:")
print("   http://localhost:8501")
print()
print("3. Verifique saldo e crie um bot!")
print()
print("="*70)
print("[SUCESSO] API Keys criptografadas e salvas no banco!")
print("="*70)
print()

