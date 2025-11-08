from fastapi_app.database import SessionLocal
from fastapi_app.models import ExchangeAPIKey
from fastapi_app.utils.encryption import decrypt_data
import ccxt

db = SessionLocal()

# Testar TODAS as exchanges do user 74
keys = db.query(ExchangeAPIKey).filter(
    ExchangeAPIKey.user_id == 74,
    ExchangeAPIKey.is_active == True
).all()

print(f"Testando {len(keys)} exchanges:\n")

for key in keys:
    print(f"{key.exchange.upper()}:")
    print(f"  Testnet: {key.is_testnet}")
    
    try:
        api_dec = decrypt_data(key.api_key_encrypted)
        secret_dec = decrypt_data(key.secret_key_encrypted)
        
        ccxt_map = {'mercadobitcoin': 'mercado', 'gateio': 'gate'}
        ccxt_name = ccxt_map.get(key.exchange, key.exchange)
        
        exchange_class = getattr(ccxt, ccxt_name)
        exchange = exchange_class({
            'apiKey': api_dec,
            'secret': secret_dec,
            'enableRateLimit': True
        })
        
        if key.is_testnet:
            exchange.set_sandbox_mode(True)
        
        balance = exchange.fetch_balance()
        usdt = balance.get('free', {}).get('USDT', 0) or 0
        
        print(f"  Saldo: ${usdt}")
        print(f"  Status: OK")
        
    except Exception as e:
        print(f"  ERRO: {str(e)[:100]}")
    
    print()

db.close()

