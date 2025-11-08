"""
Forçar criação de trade de teste
Para verificar se Dashboard atualiza
"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade
from datetime import datetime

db = SessionLocal()

# Criar trade de teste
trade = Trade(
    user_id=74,  # Seu usuário
    bot_config_id=38,  # Bot ativo
    exchange='binance',
    symbol='SOL/USDT',
    side='buy',
    entry_price=120.50,
    quantity=0.083,
    entry_time=datetime.now(),
    status='open'
)

db.add(trade)
db.commit()

print(f"[OK] Trade de TESTE criado! ID: {trade.id}")
print(f"   Symbol: {trade.symbol}")
print(f"   Preço: ${trade.entry_price}")
print()
print("Agora:")
print("  1. Acesse Dashboard: http://localhost:8501")
print("  2. Aguarde 3s")
print("  3. Trades Hoje deve incrementar!")
print("  4. Saldo deve atualizar!")
print()

db.close()

