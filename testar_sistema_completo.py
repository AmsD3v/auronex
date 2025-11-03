"""
Teste End-to-End do Sistema FastAPI
"""
import requests

print("\n" + "=" * 60)
print("  TESTE COMPLETO DO SISTEMA")
print("=" * 60)
print()

# 1. Testar Login
print("1. Testando Login...")
try:
    r = requests.post(
        'http://localhost:8001/api/auth/login',
        json={'email': 'admin@robotrader.com', 'password': 'admin123'},
        timeout=5
    )
    
    if r.status_code == 200:
        token_data = r.json()
        token = token_data.get('access_token')
        print(f"   Status: {r.status_code}")
        print(f"   Login: SUCESSO")
        print(f"   Token recebido: Sim")
    else:
        print(f"   Status: {r.status_code}")
        print(f"   Login: FALHOU")
        print(f"   Erro: {r.text}")
        token = None
        
except Exception as e:
    print(f"   ERRO: {e}")
    token = None

print()

# 2. Testar Acesso Autenticado
if token:
    print("2. Testando Acesso Autenticado...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        me = requests.get('http://localhost:8001/api/auth/me', headers=headers, timeout=5)
        
        if me.status_code == 200:
            user = me.json()
            print(f"   Status: {me.status_code}")
            print(f"   Usuario: {user.get('email')}")
            print(f"   Nome: {user.get('first_name')} {user.get('last_name')}")
        else:
            print(f"   Status: {me.status_code}")
            print(f"   ERRO: {me.text}")
            
    except Exception as e:
        print(f"   ERRO: {e}")
        
    print()
    
    # 3. Testar API Keys
    print("3. Testando API Keys...")
    try:
        keys = requests.get('http://localhost:8001/api/api-keys/', headers=headers, timeout=5)
        
        if keys.status_code == 200:
            api_keys = keys.json()
            print(f"   Status: {keys.status_code}")
            print(f"   API Keys cadastradas: {len(api_keys)}")
        else:
            print(f"   Status: {keys.status_code}")
            print(f"   ERRO: {keys.text}")
            
    except Exception as e:
        print(f"   ERRO: {e}")
        
    print()
    
    # 4. Testar Bot Configs
    print("4. Testando Bot Configurations...")
    try:
        bots = requests.get('http://localhost:8001/api/bots/', headers=headers, timeout=5)
        
        if bots.status_code == 200:
            bot_configs = bots.json()
            print(f"   Status: {bots.status_code}")
            print(f"   Bots cadastrados: {len(bot_configs)}")
        else:
            print(f"   Status: {bots.status_code}")
            print(f"   ERRO: {bots.text}")
            
    except Exception as e:
        print(f"   ERRO: {e}")
        
    print()
    
    # 5. Testar Trades
    print("5. Testando Trades...")
    try:
        trades = requests.get('http://localhost:8001/api/trades/', headers=headers, timeout=5)
        
        if trades.status_code == 200:
            trade_list = trades.json()
            print(f"   Status: {trades.status_code}")
            print(f"   Trades registrados: {len(trade_list)}")
        else:
            print(f"   Status: {trades.status_code}")
            print(f"   ERRO: {trades.text}")
            
    except Exception as e:
        print(f"   ERRO: {e}")

print()
print("=" * 60)
print("  TESTE CONCLUIDO!")
print("=" * 60)
print()
print("CREDENCIAIS DE TESTE:")
print("  Email: admin@robotrader.com")
print("  Senha: admin123")
print()
print("ACESSE:")
print("  Dashboard: http://localhost:8501")
print("  API Docs: http://localhost:8001/api/docs")
print()
print("=" * 60)

