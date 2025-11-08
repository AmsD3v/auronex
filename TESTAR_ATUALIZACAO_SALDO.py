"""
Testar se Saldo Total atualiza no Dashboard
Vou simular mudança de saldo
"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade
from datetime import datetime

db = SessionLocal()

print("="*70)
print("  TESTE: ATUALIZACAO DE SALDO")
print("="*70)
print()

# Ver trade atual
trade = db.query(Trade).filter(Trade.id == 3).first()

if trade:
    print(f"Trade #{trade.id}:")
    print(f"  Status atual: {trade.status}")
    print(f"  Entry: ${trade.entry_price}")
    print(f"  Exit: ${trade.exit_price or 'N/A'}")
    print(f"  P/L: ${trade.profit_loss or 0}")
    print()
    
    # Simular fechamento com LUCRO
    print("Simulando fechamento com LUCRO...")
    trade.exit_price = 124.50  # +3.3% de lucro
    trade.exit_time = datetime.now()
    trade.profit_loss = (124.50 - 120.50) * 0.083  # $0.33
    trade.profit_loss_percent = 3.3
    trade.status = 'closed'
    
    db.commit()
    
    print(f"[OK] Trade fechado!")
    print(f"   Exit: ${trade.exit_price}")
    print(f"   Lucro: ${trade.profit_loss:.2f}")
    print(f"   Percentual: {trade.profit_loss_percent}%")
    print()
    print("Agora:")
    print("  1. Acesse Dashboard: http://localhost:8501")
    print("  2. Aguarde 3s")
    print("  3. Saldo Total deve AUMENTAR +$0.33!")
    print("  4. Taxa Sucesso deve mostrar 100% (1 lucro)")
    print()
else:
    print("Trade nao encontrado!")

db.close()

