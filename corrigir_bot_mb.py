"""Corrigir simbolos do Bot Mercado Bitcoin"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration

db = SessionLocal()

bot = db.query(BotConfiguration).filter(BotConfiguration.id == 40).first()

if bot:
    print(f"Bot {bot.id}: {bot.name}")
    print(f"  Symbols ANTES: {bot.symbols}")
    
    # Corrigir para simbolos que MB tem
    bot.symbols = ['BTC/BRL', 'ETH/BRL', 'XRP/BRL']
    
    db.commit()
    
    print(f"  Symbols DEPOIS: {bot.symbols}")
    print("\n[OK] Bot corrigido!")
    print("\nReiniciar Bot Controller para aplicar!")
else:
    print("Bot 40 nao encontrado")

db.close()

