"""
LIMPAR capital errado dos bots
Resetar para 0 e deixar usuário configurar de novo
"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration

db = SessionLocal()

# Buscar bots com capital > 1000 (provavelmente erro)
bots_errados = db.query(BotConfiguration).filter(
    BotConfiguration.capital > 1000
).all()

print(f"Bots com capital > $1000 (provável erro):")
print("="*60)

for bot in bots_errados:
    print(f"Bot {bot.id}: {bot.name}")
    print(f"  Capital atual: ${bot.capital}")
    print(f"  Ativo: {bot.is_active}")
    print(f"  Zerando capital...")
    
    bot.capital = 0
    print(f"  ✅ Capital zerado!")
    print("-"*60)

db.commit()
db.close()

print(f"\n✅ {len(bots_errados)} bot(s) corrigido(s)!")
print("\nAgora o usuário pode configurar capital correto no Dashboard.")



