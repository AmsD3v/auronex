"""
Script para testar se os endpoints do FastAPI estão disponíveis
"""

import requests

API_URL = "http://localhost:8001"

def test_endpoints():
    """Testar endpoints"""
    
    print("=" * 60)
    print("  TESTANDO ENDPOINTS DO FASTAPI")
    print("=" * 60)
    print()
    
    # 1. Health
    print("1. Testing /health...")
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        print(f"   [OK] Status: {r.status_code}")
        print(f"   Response: {r.json()}")
    except Exception as e:
        print(f"   [ERRO] {e}")
    
    print()
    
    # 2. API Docs
    print("2. Testing /api/docs...")
    try:
        r = requests.get(f"{API_URL}/api/docs", timeout=5)
        print(f"   [OK] Status: {r.status_code}")
        print(f"   Swagger disponivel!")
    except Exception as e:
        print(f"   [ERRO] {e}")
    
    print()
    
    # 3. Exchange Balance (sem token - deve dar 401)
    print("3. Testing /api/exchange/balance...")
    try:
        r = requests.get(f"{API_URL}/api/exchange/balance", timeout=5)
        if r.status_code == 401:
            print(f"   [OK] Endpoint existe! (401 = precisa token)")
        elif r.status_code == 404:
            print(f"   [ERRO] Endpoint NAO existe! (404)")
            print(f"   Backend NAO carregou o router!")
        else:
            print(f"   [OK] Status: {r.status_code}")
            print(f"   Response: {r.text[:200]}")
    except Exception as e:
        print(f"   [ERRO] {e}")
    
    print()
    
    # 4. Listar todos os endpoints disponíveis
    print("4. Listando TODOS os endpoints...")
    try:
        r = requests.get(f"{API_URL}/openapi.json", timeout=5)
        if r.status_code == 200:
            openapi = r.json()
            paths = openapi.get('paths', {})
            
            print(f"   Total de endpoints: {len(paths)}")
            print()
            print("   Endpoints /api/exchange/:")
            for path in paths.keys():
                if '/exchange' in path:
                    print(f"      [OK] {path}")
            
            if not any('/exchange' in p for p in paths.keys()):
                print("      [ERRO] NENHUM endpoint /exchange/ encontrado!")
                print("      -> Backend nao carregou o router!")
                print("      -> REINICIE o backend!")
        else:
            print(f"   [ERRO] Status: {r.status_code}")
    except Exception as e:
        print(f"   [ERRO] {e}")
    
    print()
    print("=" * 60)
    print("  TESTE CONCLUÍDO")
    print("=" * 60)
    print()
    
    print("DIAGNOSTICO:")
    print()
    print("Se /api/exchange/balance existe (401):")
    print("  [OK] Backend carregou router corretamente!")
    print("  [OK] Dashboard React vai funcionar!")
    print()
    print("Se /api/exchange/balance NAO existe (404):")
    print("  [ERRO] Backend NAO carregou router!")
    print("  [ERRO] REINICIE completamente o backend:")
    print("     1. Ctrl+C no terminal")
    print("     2. Rodar: uvicorn fastapi_app.main:app --port 8001 --reload")
    print()

if __name__ == "__main__":
    test_endpoints()

