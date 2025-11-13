"""Fechar 3 posições que estão abertas"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade
from datetime import datetime

db = SessionLocal()

abertas = db.query(Trade).filter(Trade.status == 'open').all()

print(f"Posições ABERTAS: {len(abertas)}")
print("="*70)

for trade in abertas:
    print(f"Trade {trade.id}:")
    print(f"  Symbol: {trade.symbol}")
    print(f"  Entry: ${float(trade.entry_price):.8f}")
    print(f"  Quantity: {trade.quantity}")
    
    # ✅ Simular fechamento (take profit +3%)
    exit_price = float(trade.entry_price) * 1.03
    profit = (exit_price - float(trade.entry_price)) * trade.quantity
    
    trade.exit_price = exit_price
    trade.exit_time = datetime.now()
    trade.profit_loss = profit
    trade.status = 'closed'
    
    print(f"  Fechado: ${exit_price:.8f}")
    print(f"  Lucro: ${profit:.2f}")
    print()

db.commit()

print("="*70)
print(f"✅ {len(abertas)} posições fechadas!")
print("Trades counter vai atualizar!")
print("="*70)

db.close()

