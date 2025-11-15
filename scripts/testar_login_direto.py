#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testar Login Diretamente via API
"""

import sys
import io
import requests
import json

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*70)
print("  TESTE DE LOGIN DIRETO VIA API")
print("="*70)
print()

url = "http://localhost:8001/api/auth/login"
dados = {
    "email": "admin@robotrader.com",
    "password": "admin123"
}

print(f"URL: {url}")
print(f"Dados: {json.dumps(dados, indent=2)}")
print()
print("Enviando request...")
print()

try:
    response = requests.post(
        url,
        json=dados,
        headers={"Content-Type": "application/json"},
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        data = response.json()
        print("[OK] LOGIN FUNCIONOU!")
        print()
        print("Response:")
        print(json.dumps(data, indent=2))
        print()
        print("Access Token:", data.get('access_token', 'N/A')[:50] + "...")
        print("User ID:", data.get('user', {}).get('id'))
        print("User Email:", data.get('user', {}).get('email'))
        print()
    else:
        print("[ERRO] Login falhou!")
        print()
        print("Response:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        print()

except Exception as e:
    print(f"[ERRO] Excecao: {e}")
    print()

print("="*70)



