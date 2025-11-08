"""
EXECUTAR NO SERVIDOR - Corrigir capital impossível
"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import BotConfiguration, ExchangeAPIKey
from fastapi_app.utils.encryption import decrypt_data

db = SessionLocal()

print("="*70)
print("  CORRIGINDO CAPITAL IMPOSSÍVEL")
print("="*70)
print()

# 1. Ver bots ativos
bots_ativos = db.query(BotConfiguration).filter(
    BotConfiguration.is_active == True
).all()

print(f"Bots ATIVOS: {len(bots_ativos)}")
print()

for bot in bots_ativos:
    print(f"Bot {bot.id}: {bot.name}")
    print(f"  Capital: ${bot.capital}")
    print(f"  Exchange: {bot.exchange}")
    print(f"  Estratégia: {bot.strategy}")
    
    # Buscar saldo REAL da exchange
    try:
        api_key = db.query(ExchangeAPIKey).filter(
            ExchangeAPIKey.user_id == bot.user_id,
            ExchangeAPIKey.exchange == bot.exchange,
            ExchangeAPIKey.is_active == True
        ).first()
        
        if api_key:
            import ccxt
            
            ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate'}
            ccxt_name = ccxt_map.get(bot.exchange, bot.exchange)
            
            api_dec = decrypt_data(api_key.api_key_encrypted)
            secret_dec = decrypt_data(api_key.secret_key_encrypted)
            
            exchange_class = getattr(ccxt, ccxt_name)
            exchange = exchange_class({
                'apiKey': api_dec,
                'secret': secret_dec,
                'enableRateLimit': True
            })
            
            if api_key.is_testnet:
                exchange.set_sandbox_mode(True)
            
            balance = exchange.fetch_balance()
            usdt = balance.get('free', {}).get('USDT', 0) or 0
            
            print(f"  Saldo REAL: ${usdt}")
            
            # ✅ Se capital > saldo = IMPOSSÍVEL!
            if bot.capital and float(bot.capital) > usdt:
                print(f"  ❌ IMPOSSÍVEL! Capital (${bot.capital}) > Saldo (${usdt})")
                print(f"  ✅ ZERANDO capital...")
                bot.capital = 0
            
    except Exception as e:
        print(f"  ⚠️ Erro ao verificar saldo: {e}")
    
    print("-"*70)

db.commit()
db.close()

print()
print("✅ CORRIGIDO!")
print()
print("Agora usuário pode configurar capital correto no Dashboard.")
print()



