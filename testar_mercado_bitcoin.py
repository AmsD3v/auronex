"""Testar Mercado Bitcoin especificamente"""
from fastapi_app.database import SessionLocal
from fastapi_app.models import ExchangeAPIKey
from fastapi_app.utils.encryption import decrypt_data
import ccxt

db = SessionLocal()

key = db.query(ExchangeAPIKey).filter(
    ExchangeAPIKey.user_id == 74,
    ExchangeAPIKey.exchange == 'mercadobitcoin'
).first()

if not key:
    print("API Key Mercado Bitcoin nao encontrada!")
    db.close()
    exit()

print("API Key encontrada!")
print(f"Testnet: {key.is_testnet}")
print()

try:
    api_dec = decrypt_data(key.api_key_encrypted)
    secret_dec = decrypt_data(key.secret_key_encrypted)
    
    print("Conectando Mercado Bitcoin...")
    exchange = ccxt.mercado({
        'apiKey': api_dec,
        'secret': secret_dec,
        'enableRateLimit': True
    })
    
    print("Buscando saldo...")
    balance = exchange.fetch_balance()
    
    print("\nBalance completo:")
    print(f"Keys: {list(balance.keys())}")
    
    # Tentar várias formas
    usdt = balance.get('free', {}).get('USDT', 0)
    brl = balance.get('free', {}).get('BRL', 0)
    
    print(f"\nUSDT: ${usdt}")
    print(f"BRL: R$ {brl}")
    
    if brl > 0:
        usdt_equiv = brl / 5.0
        print(f"\nBRL convertido: ${usdt_equiv}")
    
    print("\n[OK] Saldo encontrado!")
    
except Exception as e:
    print(f"\n[ERRO] {e}")
    import traceback
    traceback.print_exc()

db.close()

