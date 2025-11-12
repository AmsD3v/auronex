"""Testar endpoint balance e ver erro exato"""
import requests

try:
    response = requests.get('http://localhost:8001/api/exchange/balance')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Erro: {e}")
    print(f"Response: {response.text if 'response' in locals() else 'N/A'}")

