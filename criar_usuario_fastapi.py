"""
Script para criar o primeiro usuário no FastAPI
Execute: python criar_usuario_fastapi.py
"""
import requests
import json
import sys

print("=" * 60)
print("  CRIAR USUÁRIO NO FASTAPI")
print("=" * 60)
print()

# Verificar se FastAPI está rodando
try:
    health = requests.get("http://localhost:8001/health", timeout=3)
    if health.status_code != 200:
        print("❌ ERRO: FastAPI não está respondendo!")
        print("   Execute primeiro: .\\INICIAR_FASTAPI.bat")
        input("\nPressione ENTER para sair...")
        sys.exit(1)
except:
    print("❌ ERRO: FastAPI não está rodando!")
    print("   Execute primeiro: .\\INICIAR_FASTAPI.bat")
    input("\nPressione ENTER para sair...")
    sys.exit(1)

print("✅ FastAPI está rodando!")
print()

# Coletar dados do usuário
try:
    email = input("Digite seu email: ").strip()
    senha = input("Digite sua senha (min. 6 caracteres): ").strip()
    primeiro_nome = input("Digite seu primeiro nome: ").strip() or "Admin"
    ultimo_nome = input("Digite seu sobrenome: ").strip() or "User"
except (EOFError, KeyboardInterrupt):
    print("\n\n❌ Operação cancelada!")
    sys.exit(1)

# Preparar dados
dados = {
    "email": email,
    "password": senha,
    "first_name": primeiro_nome,
    "last_name": ultimo_nome
}

print()
print("Criando usuário...")

try:
    # Registrar usuário
    response = requests.post(
        "http://localhost:8001/api/auth/register",
        json=dados,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print()
        print("✅ SUCESSO! Usuário criado:")
        print(f"   Email: {result.get('email')}")
        print(f"   Nome: {result.get('full_name')}")
        print(f"   ID: {result.get('id')}")
        print()
        print("Agora você pode fazer login no Dashboard:")
        print(f"   Email: {email}")
        print(f"   Senha: {senha}")
        print()
        print("Acesse: http://localhost:8501")
        
    elif response.status_code == 400:
        error = response.json()
        print()
        print("❌ ERRO:", error.get('detail', 'Erro desconhecido'))
        print()
        if "already registered" in str(error):
            print("💡 DICA: Este email já está cadastrado!")
            print("   Tente fazer login ou use outro email.")
        
    else:
        print()
        print(f"❌ ERRO: Status {response.status_code}")
        print(f"   Resposta: {response.text}")
        
except requests.exceptions.ConnectionError:
    print()
    print("❌ ERRO: Não foi possível conectar ao FastAPI!")
    print("   Certifique-se de que o FastAPI está rodando.")
    print("   Execute: .\\INICIAR_FASTAPI.bat")
    
except Exception as e:
    print()
    print(f"❌ ERRO INESPERADO: {e}")

print()
print("=" * 60)
input("Pressione ENTER para sair...")

