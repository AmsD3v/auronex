"""Verificar O QUE o dashboard DEVERIA mostrar"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade, BotConfiguration
from datetime import datetime

db = SessionLocal()

print("="*70)
print("  O QUE O DASHBOARD DEVERIA MOSTRAR")
print("="*70)
print()

# 1. TRADES HOJE
hoje = datetime.now().date()
from sqlalchemy import func
trades_hoje = db.query(Trade).filter(func.date(Trade.entry_time) == hoje).count()
print(f"1. TRADES HOJE: {trades_hoje}")

# 2. TAXA SUCESSO
fechados = db.query(Trade).filter(Trade.exit_time.isnot(None)).all()
if fechados:
    wins = sum(1 for t in fechados if t.profit_loss and float(t.profit_loss) > 0)
    taxa = (wins / len(fechados)) * 100
    print(f"2. TAXA SUCESSO: {taxa:.1f}%")
else:
    print(f"2. TAXA SUCESSO: 0%")

# 3. LUCRO TOTAL
lucro = sum(float(t.profit_loss) for t in fechados if t.profit_loss)
print(f"3. LUCRO TOTAL: ${lucro:.2f} = R$ {lucro * 5:.2f}")

# 4. BOTS ATIVOS
bots = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).count()
print(f"4. BOTS ATIVOS: {bots}")

# 5. CAPITAL INVESTIDO
bots_ativos = db.query(BotConfiguration).filter(BotConfiguration.is_active == True).all()
capital = sum(float(b.capital) for b in bots_ativos if b.capital)
print(f"5. CAPITAL INVESTIDO: ${capital:.2f} = R$ {capital * 5:.2f}")

print()
print("="*70)
print("DASHBOARD DEVE MOSTRAR:")
print(f"  Saldo Total: R$ 20,00 (das exchanges)")
print(f"  Lucro Liquido: +R$ {lucro * 5:.2f}")
print(f"  Trades Hoje: {trades_hoje}")
print(f"  Taxa Sucesso: {taxa:.1f}%" if fechados else "  Taxa Sucesso: 0%")
print(f"  Bots Ativos: {bots}")
print("="*70)

db.close()

