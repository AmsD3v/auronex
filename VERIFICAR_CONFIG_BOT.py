"""
Verificar se bot le configuracoes do Dashboard corretamente
"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration

db = SessionLocal()

print("="*70)
print("  CONFIGURACOES DOS BOTS NO BANCO")
print("="*70)
print()

bots = db.query(BotConfiguration).all()

for bot in bots:
    print(f"ID: {bot.id}")
    print(f"Nome: {bot.name}")
    print(f"Exchange: {bot.exchange.upper()}")
    print(f"Cryptos: {bot.symbols}")
    print(f"Estrategia: {bot.strategy}")
    print(f"Timeframe: {bot.timeframe}")
    print(f"Capital: ${bot.capital}")
    print(f"Stop Loss: {bot.stop_loss_percent}%")
    print(f"Take Profit: {bot.take_profit_percent}%")
    print(f"Ativo: {'SIM' if bot.is_active else 'NAO'}")
    print(f"Testnet: {'SIM' if hasattr(bot, 'is_testnet') and bot.is_testnet else 'NAO'}")
    
    # NOVO: Velocidade
    if hasattr(bot, 'analysis_interval'):
        vel = bot.analysis_interval
        modo = "Scalper (1s)" if vel == 1 else "Cacador (3s)" if vel == 3 else "Ultra Rapido (5s)"
        print(f"Velocidade: {vel}s ({modo})")
    
    if hasattr(bot, 'hunter_mode'):
        print(f"Modo Cacador: {'SIM' if bot.hunter_mode else 'NAO'}")
    
    print("-"*70)

print()
print(f"Total: {len(bots)} bots")
print(f"Ativos: {len([b for b in bots if b.is_active])}")
print()

db.close()



