#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurar API Keys das Exchanges
Script interativo e seguro
"""

import sys
import io
from pathlib import Path
from getpass import getpass

# Fix encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Adicionar raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("="*70)
print("  CONFIGURADOR DE API KEYS - AURONEX")
print("="*70)
print()

# Verificar se .env existe
import os
from dotenv import load_dotenv

load_dotenv()

encryption_key = os.getenv('ENCRYPTION_KEY')
if not encryption_key:
    print("[ERRO] ENCRYPTION_KEY nao configurada no .env!")
    print()
    print("Execute primeiro:")
    print("1. Crie o arquivo .env (copie de .env.local)")
    print("2. Execute este script novamente")
    print()
    sys.exit(1)

print("[OK] ENCRYPTION_KEY configurada")
print()

# Importar módulos
try:
    from fastapi_app.database import SessionLocal
    from fastapi_app.models import User, ExchangeAPIKey
    from fastapi_app.utils.encryption import encrypt_data
except Exception as e:
    print(f"[ERRO] Falha ao importar modulos: {e}")
    print()
    print("Certifique-se que:")
    print("1. Voce esta na raiz do projeto")
    print("2. .env esta configurado")
    print("3. Dependencias estao instaladas (pip install -r requirements.txt)")
    print()
    sys.exit(1)

print("[OK] Modulos importados")
print()

# Conectar banco
db = SessionLocal()

# Buscar usuário
print("Buscando usuario no banco...")
user = db.query(User).filter(User.email == "admin@robotrader.com").first()

if not user:
    print("[ERRO] Usuario admin@robotrader.com nao encontrado!")
    print()
    print("Crie o usuario primeiro ou altere o email no script.")
    print()
    db.close()
    sys.exit(1)

print(f"[OK] Usuario encontrado: {user.email} (ID: {user.id})")
print()

# Exchanges disponíveis
EXCHANGES = [
    "binance",
    "bybit",
    "mercadobitcoin",
    "okx",
    "kraken",
    "gateio",
    "kucoin",
    "foxbit",
    "novadax"
]

print("="*70)
print("  EXCHANGES DISPONIVEIS:")
print("="*70)
for i, ex in enumerate(EXCHANGES, 1):
    print(f"{i}. {ex.upper()}")
print()

# Menu
while True:
    print("Opcoes:")
    print("1. Adicionar nova API Key")
    print("2. Listar API Keys existentes")
    print("3. Remover API Key")
    print("0. Sair")
    print()
    
    opcao = input("Escolha uma opcao: ").strip()
    print()
    
    if opcao == "0":
        print("Saindo...")
        break
    
    elif opcao == "1":
        # Adicionar nova API Key
        print("="*70)
        print("  ADICIONAR NOVA API KEY")
        print("="*70)
        print()
        
        # Selecionar exchange
        print("Selecione a exchange:")
        for i, ex in enumerate(EXCHANGES, 1):
            print(f"{i}. {ex.upper()}")
        print()
        
        try:
            exchange_num = int(input("Numero da exchange: ").strip())
            if exchange_num < 1 or exchange_num > len(EXCHANGES):
                print("[ERRO] Numero invalido!")
                print()
                continue
            
            exchange_name = EXCHANGES[exchange_num - 1]
            print(f"[OK] Exchange selecionada: {exchange_name.upper()}")
            print()
            
        except ValueError:
            print("[ERRO] Digite um numero valido!")
            print()
            continue
        
        # Verificar se já existe
        existing = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == user.id,
            ExchangeAPIKey.exchange == exchange_name
        ).first()
        
        if existing:
            print(f"[AVISO] Ja existe uma API Key para {exchange_name.upper()}!")
            resposta = input("Deseja sobrescrever? (s/n): ").lower()
            if resposta not in ['s', 'sim', 'y', 'yes']:
                print("Operacao cancelada.")
                print()
                continue
            
            # Deletar existente
            db.delete(existing)
            db.commit()
            print("[OK] API Key antiga removida")
            print()
        
        # Solicitar credenciais
        print(f"Digite as credenciais da {exchange_name.upper()}:")
        print()
        
        api_key = getpass(f"API Key: ").strip()
        if not api_key:
            print("[ERRO] API Key nao pode ser vazia!")
            print()
            continue
        
        secret_key = getpass(f"Secret Key: ").strip()
        if not secret_key:
            print("[ERRO] Secret Key nao pode ser vazia!")
            print()
            continue
        
        # Testnet?
        is_testnet_input = input("É Testnet? (s/n, padrão: s): ").lower()
        is_testnet = is_testnet_input in ['s', 'sim', 'y', 'yes', '']
        
        print()
        print("Criptografando credenciais...")
        
        # Criptografar
        try:
            api_key_encrypted = encrypt_data(api_key)
            secret_encrypted = encrypt_data(secret_key)
            
            print("[OK] Credenciais criptografadas")
            print()
            
        except Exception as e:
            print(f"[ERRO] Falha ao criptografar: {e}")
            print()
            continue
        
        # Salvar no banco
        print("Salvando no banco de dados...")
        
        new_api_key = ExchangeAPIKey(
            user_id=user.id,
            exchange=exchange_name,
            api_key_encrypted=api_key_encrypted,
            secret_key_encrypted=secret_encrypted,
            is_testnet=is_testnet,
            is_active=True
        )
        
        db.add(new_api_key)
        
        try:
            db.commit()
            print(f"[OK] API Key salva com sucesso!")
            print()
            print(f"Exchange: {exchange_name.upper()}")
            print(f"Testnet: {'Sim' if is_testnet else 'Nao'}")
            print(f"Status: Ativa")
            print()
            
        except Exception as e:
            db.rollback()
            print(f"[ERRO] Falha ao salvar: {e}")
            print()
    
    elif opcao == "2":
        # Listar API Keys
        print("="*70)
        print("  API KEYS CONFIGURADAS")
        print("="*70)
        print()
        
        api_keys = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == user.id
        ).all()
        
        if not api_keys:
            print("Nenhuma API Key configurada.")
            print()
        else:
            for i, key in enumerate(api_keys, 1):
                status = "Ativa" if key.is_active else "Inativa"
                testnet = "Testnet" if key.is_testnet else "Producao"
                print(f"{i}. {key.exchange.upper()}")
                print(f"   ID: {key.id}")
                print(f"   Tipo: {testnet}")
                print(f"   Status: {status}")
                print(f"   Criada: {key.created_at.strftime('%d/%m/%Y %H:%M')}")
                print()
    
    elif opcao == "3":
        # Remover API Key
        print("="*70)
        print("  REMOVER API KEY")
        print("="*70)
        print()
        
        api_keys = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == user.id
        ).all()
        
        if not api_keys:
            print("Nenhuma API Key configurada.")
            print()
            continue
        
        print("API Keys disponiveis:")
        for i, key in enumerate(api_keys, 1):
            print(f"{i}. {key.exchange.upper()} (ID: {key.id})")
        print()
        
        try:
            num = int(input("Numero da API Key para remover: ").strip())
            if num < 1 or num > len(api_keys):
                print("[ERRO] Numero invalido!")
                print()
                continue
            
            key_to_remove = api_keys[num - 1]
            
            print(f"Remover {key_to_remove.exchange.upper()}?")
            confirma = input("Digite 'CONFIRMAR' para remover: ").strip()
            
            if confirma == "CONFIRMAR":
                db.delete(key_to_remove)
                db.commit()
                print(f"[OK] API Key {key_to_remove.exchange.upper()} removida!")
                print()
            else:
                print("Operacao cancelada.")
                print()
                
        except ValueError:
            print("[ERRO] Digite um numero valido!")
            print()
    
    else:
        print("[ERRO] Opcao invalida!")
        print()

db.close()

print("="*70)
print("  CONFIGURACAO FINALIZADA")
print("="*70)
print()
print("API Keys configuradas com sucesso!")
print()
print("Proximos passos:")
print("1. Reinicie os servicos")
print("2. Teste conexao com exchange")
print("3. Crie um bot")
print()






