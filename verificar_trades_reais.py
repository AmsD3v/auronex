"""Verificar se trades sao REAIS ou manuais"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade, User

db = SessionLocal()

# Ver todos trades
trades = db.query(Trade).order_by(Trade.id).all()

print("="*70)
print(f"  ANALISE DOS {len(trades)} TRADES")
print("="*70)
print()

# Agrupar por minuto
from datetime import datetime
from collections import defaultdict

trades_por_minuto = defaultdict(int)

for t in trades:
    minuto = t.entry_time.strftime('%Y-%m-%d %H:%M')
    trades_por_minuto[minuto] += 1

print("TRADES POR MINUTO:")
for minuto, count in sorted(trades_por_minuto.items()):
    print(f"  {minuto}: {count} trade(s)")

print()
print("ANALISE:")
print(f"  Primeiro trade: {trades[0].entry_time}")
print(f"  Ultimo trade: {trades[-1].entry_time}")
print()

# Se todos no mesmo minuto = MANUAL
if len(trades_por_minuto) <= 2:
    print("  ❌ PROVAVEL: Trades MANUAIS (todos no mesmo minuto)")
else:
    print("  ✅ PROVAVEL: Trades REAIS (espalhados no tempo)")

print()

# Ver user
user = db.query(User).filter(User.id == 74).first()
print(f"USER 74:")
print(f"  Email: {user.email}")
print(f"  Nome: '{user.first_name}' '{user.last_name}'")
print(f"  Vazio? {not user.first_name or user.first_name == ''}")

db.close()

