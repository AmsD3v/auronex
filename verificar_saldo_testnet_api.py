"""
Script para verificar saldo da Binance Testnet via API
Use este script se a interface web estiver confusa
"""

import os
import sys
import django

sys.path.insert(0, 'I:\\Robo\\saas')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saas.settings')
django.setup()

from users.models import ExchangeAPIKey
import ccxt

print("\n" + "="*60)
print("  VERIFICACAO DE SALDO - BINANCE TESTNET")
print("="*60 + "\n")

# Buscar API Key do banco
try:
    api_key_obj = ExchangeAPIKey.objects.filter(
        exchange='binance',
        is_testnet=True,
        is_active=True
    ).first()
    
    if not api_key_obj:
        print("ERRO: Nenhuma API Key testnet encontrada!")
        print("\nAdicione API Key em:")
        print("http://localhost:8001/admin/users/exchangeapikey/add/")
        sys.exit(1)
    
    print(f"API Key encontrada para usuario: {api_key_obj.user.email}")
    print(f"Exchange: {api_key_obj.exchange}")
    print(f"Testnet: {api_key_obj.is_testnet}")
    print()
    
    # Conectar na Binance Testnet
    print("Conectando na Binance Testnet...")
    
    exchange = ccxt.binance({
        'apiKey': api_key_obj.api_key,
        'secret': api_key_obj.secret_key,
        'enableRateLimit': True,
    })
    
    exchange.set_sandbox_mode(True)
    
    print("Conexao estabelecida!")
    print()
    
    # Buscar saldo
    print("Buscando saldo...")
    balance = exchange.fetch_balance()
    
    print("\n" + "="*60)
    print("  SALDO DA SUA CONTA TESTNET")
    print("="*60 + "\n")
    
    # Mostrar principais moedas
    principais = ['USDT', 'BNB', 'BTC', 'ETH', 'BRL']
    
    saldo_encontrado = False
    
    for moeda in principais:
        if moeda in balance['total'] and balance['total'][moeda] > 0:
            total = balance['total'][moeda]
            livre = balance['free'][moeda]
            usado = balance['used'][moeda]
            
            print(f"{moeda}:")
            print(f"  Total:      {total:,.8f}")
            print(f"  Disponivel: {livre:,.8f}")
            print(f"  Em uso:     {usado:,.8f}")
            print()
            
            saldo_encontrado = True
    
    if saldo_encontrado:
        print("="*60)
        print("  FUNDOS DISPONIVEIS!")
        print("="*60)
        print("\nVoce TEM saldo na testnet!")
        print("Bot pode operar normalmente!")
        print()
    else:
        print("="*60)
        print("  NENHUM SALDO ENCONTRADO")
        print("="*60)
        print("\nVoce precisa solicitar fundos no Faucet:")
        print("https://testnet.binance.vision/en/faucet")
        print()
    
except Exception as e:
    print(f"\nERRO ao verificar saldo: {e}")
    print("\nVerifique:")
    print("1. API Key esta correta")
    print("2. API Key tem permissao de leitura")
    print("3. is_testnet = True")
    print()

