"""Corrigir Bot 52 Mercado Bitcoin"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration

db = SessionLocal()

bot = db.query(BotConfiguration).filter(BotConfiguration.id == 52).first()

if bot:
    print(f"Bot {bot.id}: {bot.name}")
    print(f"  Exchange: {bot.exchange}")
    print(f"  Symbols ANTES: {bot.symbols}")
    
    # Corrigir para symbols que MB TEM
    bot.symbols = ['BTC/BRL', 'ETH/BRL', 'XRP/BRL']
    
    db.commit()
    
    print(f"  Symbols DEPOIS: {bot.symbols}")
    print("\n[OK] Corrigido!")
else:
    print("Bot 52 nao encontrado")

db.close()

