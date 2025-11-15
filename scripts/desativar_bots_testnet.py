import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration

db = SessionLocal()

# Desativar TODOS bots testnet
bots = db.query(BotConfiguration).filter(BotConfiguration.is_testnet == True).all()

print(f"Desativando {len(bots)} bots testnet...")

for bot in bots:
    bot.is_active = False
    bot.is_testnet = False  # Mudar para producao
    print(f"  Bot {bot.id}: {bot.name} - Desativado e mudado para producao")

db.commit()
print("OK - Bots atualizados")
db.close()

