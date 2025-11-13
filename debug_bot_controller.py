"""Debug: Por que bot não faz mais trades?"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration, Trade
from datetime import datetime, timedelta
from sqlalchemy import func

db = SessionLocal()

print("="*70)
print("  DEBUG BOT CONTROLLER")
print("="*70)
print()

# 1. Bots ativos
bots = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all()
print(f"1. BOTS ATIVOS: {len(bots)}")
for bot in bots:
    print(f"   Bot {bot.id}: {bot.name}")
    print(f"     Exchange: {bot.exchange}")
    print(f"     Capital: ${bot.capital}")
    print(f"     Symbols: {bot.symbols}")
    print(f"     Testnet: {bot.is_testnet}")
print()

# 2. Trades nas últimas 24h
desde = datetime.now() - timedelta(hours=24)
trades_24h = db.query(Trade).filter(Trade.entry_time >= desde).count()
print(f"2. TRADES ÚLTIMAS 24H: {trades_24h}")
print()

# 3. Trades hoje
hoje = datetime.now().date()
trades_hoje = db.query(Trade).filter(func.date(Trade.entry_time) == hoje).count()
print(f"3. TRADES HOJE: {trades_hoje}")
print()

# 4. Posições abertas
abertas = db.query(Trade).filter(Trade.status == 'open').count()
print(f"4. POSIÇÕES ABERTAS: {abertas}")
print()

# 5. Último trade
ultimo = db.query(Trade).order_by(Trade.entry_time.desc()).first()
if ultimo:
    print(f"5. ÚLTIMO TRADE:")
    print(f"   ID: {ultimo.id}")
    print(f"   Symbol: {ultimo.symbol}")
    print(f"   Hora: {ultimo.entry_time}")
    print(f"   Status: {ultimo.status}")
else:
    print(f"5. NENHUM TRADE!")

print()
print("="*70)
print("CONCLUSÃO:")
if len(bots) == 0:
    print("  ❌ Nenhum bot ativo - Ative um bot!")
elif trades_24h == 0:
    print("  ❌ Bot não fez trades nas últimas 24h")
    print("  Possíveis causas:")
    print("    - Bot Controller NÃO está rodando")
    print("    - Sem oportunidades no mercado")
    print("    - Capital insuficiente")
else:
    print(f"  ✅ Bot funcionando ({trades_24h} trades em 24h)")
print("="*70)

db.close()

