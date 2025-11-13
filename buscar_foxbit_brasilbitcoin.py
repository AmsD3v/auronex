"""Buscar listas reais Foxbit e BrasilBitcoin"""
import requests

print("="*70)
print("  BUSCANDO LISTAS REAIS")
print("="*70)
print()

# Foxbit
try:
    print("1. FOXBIT:")
    r = requests.get('https://api.foxbit.com.br/v3/markets', timeout=5)
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, list):
            symbols = [m.get('symbol', '').replace('_', '/') for m in data]
            brl = [s for s in symbols if 'BRL' in s]
            print(f"   Total: {len(symbols)}")
            print(f"   BRL: {len(brl)}")
            print(f"   Primeiros 20:")
            [print(f"     {s}") for s in sorted(brl)[:20]]
except Exception as e:
    print(f"   Erro: {e}")

print()

# BrasilBitcoin
try:
    print("2. BRASILBITCOIN:")
    r = requests.get('https://brasilbitcoin.com.br/api/tickers', timeout=5)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"   Data type: {type(data)}")
        print(f"   Keys: {list(data.keys())[:10] if isinstance(data, dict) else 'N/A'}")
except Exception as e:
    print(f"   Erro: {e}")

print()
print("="*70)

