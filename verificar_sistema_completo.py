"""Verificacao COMPLETA do sistema"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration, Trade, User

db = SessionLocal()

print("="*70)
print("  VERIFICACAO COMPLETA DO SISTEMA")
print("="*70)
print()

# 1. BOTS ATIVOS
print("1. BOTS ATIVOS:")
bots = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all()
for bot in bots:
    print(f"  Bot {bot.id}: {bot.name}")
    print(f"    Exchange: {bot.exchange}")
    print(f"    Testnet: {bot.is_testnet}")
    print(f"    Capital: ${bot.capital}")
    print(f"    Symbols: {bot.symbols}")
print()

# 2. TRADES HOJE
from datetime import datetime
hoje = datetime.now().date()
from sqlalchemy import func

trades_hoje = db.query(Trade).filter(func.date(Trade.entry_time) == hoje).count()
print(f"2. TRADES HOJE: {trades_hoje}")
print()

# 3. TRADES FECHADOS
fechados = db.query(Trade).filter(Trade.status == 'closed').all()
lucro = sum(float(t.profit_loss) for t in fechados if t.profit_loss)
print(f"3. TRADES FECHADOS: {len(fechados)}")
print(f"   Lucro total: ${lucro:.2f}")
print()

# 4. POSICOES ABERTAS
abertas = db.query(Trade).filter(Trade.status == 'open').count()
print(f"4. POSICOES ABERTAS: {abertas}")
print()

# 5. USUARIOS
users = db.query(User).all()
print(f"5. USUARIOS: {len(users)}")
for u in users:
    print(f"  {u.id}: {u.email} ({u.first_name})")
print()

print("="*70)
print("CONCLUSAO:")
print(f"  Bots ativos: {len(bots)}")
print(f"  Trades hoje: {trades_hoje}")
print(f"  Lucro total: ${lucro:.2f}")
print(f"  Bot funcionando: {'SIM' if len(bots) > 0 else 'NAO'}")
print("="*70)

db.close()

