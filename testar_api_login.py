"""Testar se API /auth/login retorna user"""
import requests
import json

response = requests.post(
    'http://localhost:8001/api/auth/login/',
    json={'email': 'admin@robotrader.com', 'password': 'admin123'}
)

print(f"Status: {response.status_code}")
print("\nResponse:")
data = response.json()
print(json.dumps(data, indent=2))

print("\n" + "="*50)
print("ANALISE:")
print(f"  Tem 'user'? {'user' in data}")
print(f"  Tem 'access_token'? {'access_token' in data}")

if 'user' in data:
    print(f"\nUSER:")
    print(f"  email: {data['user'].get('email')}")
    print(f"  first_name: {data['user'].get('first_name')}")
else:
    print("\n[PROBLEMA] API NAO retorna campo 'user'!")
    print("Corrigir: fastapi_app/routers/auth.py linha 75")

