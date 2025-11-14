"""Testar API Top 5"""
import requests

print("Testando API Top 5 Gainers...")
print("="*70)

try:
    r = requests.get('http://localhost:8001/api/market/top-gainers?period=24h', timeout=5)
    print(f"Status: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"Source: {data.get('source', 'N/A')}")
        print(f"Total coins: {len(data.get('data', []))}")
        print()
        
        for i, coin in enumerate(data.get('data', []), 1):
            print(f"{i}. {coin['symbol']:8} {coin['name']:20} ${coin['price']:12.2f}  +{coin['change_24h']:6.2f}%")
    else:
        print(f"Erro: {r.text}")
        
except Exception as e:
    print(f"Erro: {e}")

print("="*70)

