"""
Ver TODOS os trades que o bot já fez
Histórico completo
"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import Trade

db = SessionLocal()

trades = db.query(Trade).order_by(Trade.id.desc()).all()

print("="*70)
print(f"  HISTÓRICO DE TRADES ({len(trades)} total)")
print("="*70)
print()

if len(trades) == 0:
    print("Nenhum trade encontrado!")
    print()
    print("Bot pode não estar:")
    print("  1. Rodando (Bot Controller parado)")
    print("  2. Encontrando oportunidades (confidence baixa)")
    print("  3. Salvando no banco (erro de código)")
else:
    for trade in trades:
        print(f"Trade #{trade.id}")
        print(f"  Bot: {trade.bot_config_id}")
        print(f"  User: {trade.user_id}")
        print(f"  Symbol: {trade.symbol}")
        print(f"  Side: {trade.side.upper()}")
        print(f"  Preço entrada: ${trade.entry_price}")
        if trade.exit_price:
            print(f"  Preço saída: ${trade.exit_price}")
            print(f"  Lucro/Perda: ${trade.profit_loss}")
        print(f"  Status: {trade.status}")
        print(f"  Data: {trade.entry_time}")
        print("-"*70)

db.close()

print()
print("VERIFICAR:")
print("  Bot Controller rodando? ps aux | grep bot_controller")
print("  Logs do bot: tail -f logs/bot_controller.log")
print()

