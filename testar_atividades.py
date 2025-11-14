"""Testar endpoint atividades"""
import requests

r = requests.get('http://localhost:8001/api/bot-activity/recent')
print(f"Status: {r.status_code}")
print(f"Atividades: {len(r.json())}")

for a in r.json()[:5]:
    print(f"  {a['symbol']}: {a['action']} (Bot: {a['bot_name']})")

