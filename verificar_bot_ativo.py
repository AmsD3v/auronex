"""Ver se tem bot ativo"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration

db = SessionLocal()

bots = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all()

print(f"Bots ATIVOS: {len(bots)}")
for bot in bots:
    print(f"  Bot {bot.id}: {bot.name}")
    print(f"    Exchange: {bot.exchange}")
    print(f"    Symbols: {bot.symbols}")
    print(f"    Capital: ${bot.capital}")

db.close()

if len(bots) == 0:
    print("\nNENHUM bot ativo!")
    print("Ative um bot no Dashboard para testar!")


