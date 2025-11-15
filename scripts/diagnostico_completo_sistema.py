#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico Completo do Sistema
Verifica tudo e mostra status
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
print("  DIAGNOSTICO COMPLETO DO SISTEMA")
print("="*70)
print()

from fastapi_app.database import SessionLocal
from fastapi_app.models import User, BotConfiguration, ExchangeAPIKey, Trade

db = SessionLocal()

# 1. USUÁRIOS
print("[1/5] USUARIOS:")
users = db.query(User).all()
print(f"  Total: {len(users)}")
for u in users:
    print(f"  - {u.email} (ID: {u.id}) - Ativo: {u.is_active}")
print()

# 2. API KEYS
print("[2/5] API KEYS:")
api_keys = db.query(ExchangeAPIKey).all()
print(f"  Total: {len(api_keys)}")
for key in api_keys:
    user = db.query(User).filter(User.id == key.user_id).first()
    status = "Ativa" if key.is_active else "Inativa"
    testnet = "Testnet" if key.is_testnet else "Prod"
    print(f"  - {key.exchange.upper()} ({testnet}) - User: {user.email if user else 'N/A'} - {status}")
print()

# 3. BOTS
print("[3/5] BOTS:")
bots = db.query(BotConfiguration).all()
print(f"  Total: {len(bots)}")
for bot in bots:
    user = db.query(User).filter(User.id == bot.user_id).first()
    status = "ATIVO" if bot.is_active else "Pausado"
    print(f"  - Bot {bot.id}: {bot.name}")
    print(f"    User: {user.email if user else 'N/A'}")
    print(f"    Exchange: {bot.exchange}")
    print(f"    Capital: ${float(bot.capital or 0):.2f}")
    print(f"    Status: {status}")
print()

# 4. TRADES
print("[4/5] TRADES:")
trades = db.query(Trade).all()
print(f"  Total: {len(trades)}")

trades_hoje = db.query(Trade).filter(
    Trade.entry_time >= db.func.date('now')
).count()
print(f"  Hoje: {trades_hoje}")

trades_abertos = db.query(Trade).filter(Trade.status == 'open').count()
print(f"  Abertos: {trades_abertos}")

trades_fechados = db.query(Trade).filter(Trade.status == 'closed').count()
print(f"  Fechados: {trades_fechados}")
print()

# 5. TESTAR ENDPOINTS
print("[5/5] TESTANDO ENDPOINTS:")
print()

import requests

base_url = "http://localhost:8001"

# Login para pegar token
print("  [a] Fazendo login...")
login_resp = requests.post(f"{base_url}/api/auth/login", json={
    "email": "admin@robotrader.com",
    "password": "admin123"
})

if login_resp.status_code == 200:
    token = login_resp.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    print("  [OK] Token obtido")
    print()
    
    # Testar /api/bots/
    print("  [b] Testando GET /api/bots/")
    bots_resp = requests.get(f"{base_url}/api/bots/", headers=headers)
    print(f"      Status: {bots_resp.status_code}")
    if bots_resp.status_code == 200:
        data = bots_resp.json()
        print(f"      Bots: {data.get('total', 0)}")
        print("      [OK] Endpoint funciona!")
    else:
        print(f"      [ERRO] {bots_resp.text[:100]}")
    print()
    
    # Testar /api/exchange/balance
    print("  [c] Testando GET /api/exchange/balance")
    balance_resp = requests.get(f"{base_url}/api/exchange/balance", headers=headers)
    print(f"      Status: {balance_resp.status_code}")
    if balance_resp.status_code == 200:
        data = balance_resp.json()
        print(f"      Saldo USDT: ${data.get('total_usd', 0):.2f}")
        print("      [OK] Endpoint funciona!")
    else:
        print(f"      [ERRO] {balance_resp.text[:100]}")
    print()
    
    # Testar /api/trades/stats
    print("  [d] Testando GET /api/trades/stats")
    stats_resp = requests.get(f"{base_url}/api/trades/stats", headers=headers)
    print(f"      Status: {stats_resp.status_code}")
    if stats_resp.status_code == 200:
        data = stats_resp.json()
        print(f"      Total trades: {data.get('total_trades', 0)}")
        print("      [OK] Endpoint funciona!")
    else:
        print(f"      [ERRO] {stats_resp.text[:100]}")
    print()
    
else:
    print(f"  [ERRO] Login falhou: {login_resp.status_code}")
    print(f"  {login_resp.text[:200]}")
    print()

db.close()

print("="*70)
print("  DIAGNOSTICO COMPLETO!")
print("="*70)
print()



