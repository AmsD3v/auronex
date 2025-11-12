"""Ver trades fechados e lucro total"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade

db = SessionLocal()

fechados = db.query(Trade).filter(Trade.status == 'closed').all()

print(f"Trades FECHADOS: {len(fechados)}")
print("="*70)

lucro_total = 0

for t in fechados:
    lucro = float(t.profit_loss) if t.profit_loss else 0
    lucro_total += lucro
    
    print(f"Trade {t.id}:")
    print(f"  Symbol: {t.symbol}")
    print(f"  Entry: ${float(t.entry_price):.8f}")
    exit_p = float(t.exit_price) if t.exit_price else 0
    print(f"  Exit: ${exit_p:.8f}")
    print(f"  Lucro: ${lucro:.2f}")
    print()

print("="*70)
print(f"LUCRO TOTAL: ${lucro_total:.2f}")
print("="*70)

db.close()

