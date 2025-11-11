"""Corrigir bot 40 DEFINITIVAMENTE"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration

db = SessionLocal()

bot = db.query(BotConfiguration).filter(BotConfiguration.id == 40).first()

print(f"Bot 40 ANTES:")
print(f"  Symbols: {bot.symbols}")

# SUBSTITUIR COMPLETAMENTE (nao adicionar)
bot.symbols = ['BTC/BRL', 'ETH/BRL', 'XRP/BRL']

db.commit()

print(f"\nBot 40 DEPOIS:")
print(f"  Symbols: {bot.symbols}")

print("\n[OK] CORRIGIDO!")
print("\nREINICIE Bot Controller!")

db.close()

