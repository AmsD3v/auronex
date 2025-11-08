"""Verificar estado do sistema"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration, Trade

db = SessionLocal()

print("="*60)
print("ESTADO DO SISTEMA")
print("="*60)
print()

# Bots ativos
bots_ativos = db.query(BotConfiguration).filter(
    BotConfiguration.is_active == True
).all()

print(f"Bots ATIVOS: {len(bots_ativos)}")
for bot in bots_ativos:
    print(f"  Bot {bot.id}: {bot.name} ({bot.exchange.upper()})")
print()

# Trades
trades = db.query(Trade).all()
print(f"Trades no banco: {len(trades)}")
for trade in trades[-5:]:
    print(f"  Trade {trade.id}: {trade.symbol} - Bot {trade.bot_config_id}")
print()

db.close()

print("CONCLUSAO:")
if len(bots_ativos) == 0:
    print("  Nenhum bot ativo - Bot Controller nao vai operar!")
    print("  SOLUCAO: Ative um bot no Dashboard")
else:
    print(f"  {len(bots_ativos)} bot(s) ativo(s) - Bot Controller deve estar operando")
    
if len(trades) == 0:
    print("  Nenhum trade salvo - Bot ainda nao executou trades OU nao esta salvando")
else:
    print(f"  {len(trades)} trade(s) salvos - Sistema funcionando!")






