"""Testar CoinCap API"""
import requests

r = requests.get('https://api.coincap.io/v2/assets?limit=100')
data = r.json()['data']

# Ordenar por ganho
sorted_data = sorted(data, key=lambda x: float(x.get('changePercent24Hr', 0)), reverse=True)[:5]

print("CoinCap Top 5 Gainers 24h:")
print("="*70)
for coin in sorted_data:
    print(f"{coin['symbol']:8} {coin['name']:20} ${float(coin['priceUsd']):12.2f}  +{float(coin['changePercent24Hr']):6.2f}%")
print("="*70)
print(f"\nFonte: CoinCap.io (SEM LIMITE!)")
print(f"Attribution: Data provided by CoinCap.io")

