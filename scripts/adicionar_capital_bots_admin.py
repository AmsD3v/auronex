#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adicionar Capital nos Bots do Admin
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
from fastapi_app.models import User, BotConfiguration

print("="*70)
print("  ADICIONAR CAPITAL NOS BOTS DO ADMIN")
print("="*70)
print()

db = SessionLocal()

# Buscar admin
admin = db.query(User).filter(User.email == "admin@robotrader.com").first()

if not admin:
    print("[ERRO] Admin nao encontrado!")
    db.close()
    sys.exit(1)

print(f"[OK] Admin encontrado: {admin.email} (ID: {admin.id})")
print()

# Buscar bots do admin
bots = db.query(BotConfiguration).filter(
    BotConfiguration.user_id == admin.id
).all()

print(f"Bots do admin: {len(bots)}")
print()

if not bots:
    print("[INFO] Admin nao tem bots.")
    print("Crie bots pelo dashboard primeiro.")
    db.close()
    sys.exit(0)

# Atualizar capital
capitals = {
    'binance': 10.0,  # $10 para Binance
    'bybit': 5.0,     # $5 para Bybit
    'mercadobitcoin': 5.0,  # $5 para MB
}

for bot in bots:
    capital_sugerido = capitals.get(bot.exchange, 5.0)
    
    print(f"Bot {bot.id}: {bot.name}")
    print(f"  Exchange: {bot.exchange}")
    print(f"  Capital atual: ${float(bot.capital or 0):.2f}")
    print(f"  Capital sugerido: ${capital_sugerido:.2f}")
    
    # Atualizar
    bot.capital = capital_sugerido
    print(f"  [OK] Capital atualizado para ${capital_sugerido:.2f}")
    print()

# Salvar
db.commit()

print("="*70)
print("  CAPITAIS ATUALIZADOS!")
print("="*70)
print()

# Mostrar resumo
print("Resumo:")
for bot in bots:
    print(f"  - {bot.name} ({bot.exchange}): ${float(bot.capital):.2f}")
print()

print("Total capital alocado: ${:.2f}".format(sum(float(b.capital) for b in bots)))
print()
print("Agora voce pode ativar os bots!")
print()

db.close()



