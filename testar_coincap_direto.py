"""Testar CoinCap direto"""
import requests

print("Testando CoinCap API diretamente...")
print("="*70)

try:
    # SEM header (CoinCap não precisa)
    r = requests.get('https://api.coincap.io/v2/assets?limit=5', timeout=5)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        coins = data['data']
        
        # Ordenar por ganho
        sorted_coins = sorted(coins, key=lambda x: float(x.get('changePercent24Hr', 0)), reverse=True)
        
        print("Top 5 Gainers:")
        for coin in sorted_coins:
            print(f"  {coin['symbol']:8} {coin['name']:20} +{float(coin['changePercent24Hr']):.2f}%")
    else:
        print(f"Erro: {r.text}")
        
except Exception as e:
    print(f"Erro: {e}")

print("="*70)
print("\nCoinCap NÃO precisa Authorization header!")
print("API Key é opcional (apenas para rate limit maior)")

