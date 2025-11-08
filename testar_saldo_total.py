"""Testar se saldo total soma todas exchanges"""
import requests

# Fazer request SEM exchange param = deve somar todas
response = requests.get('http://localhost:8001/api/exchange/balance', 
                       headers={'Authorization': 'Bearer test'})

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Total USD: ${data.get('total_usd', 0)}")
    print(f"Exchange: {data.get('exchange')}")
    print(f"Saldo: ${data}")
else:
    print(f"Erro: {response.text}")

